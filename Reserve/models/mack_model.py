import pandas as pd
import numpy as np

def run_mack_model(input_path, output_path_long, output_path_triangle):
    # Step 1: Load input triangle
    triangle_df = pd.read_csv(input_path, index_col=0)
    origin_periods = triangle_df.index
    dev_periods = triangle_df.columns.astype(int)
    n, m = triangle_df.shape
    C = triangle_df.to_numpy(dtype=float)

    # Step 2: Estimate development factors f_j
    f = []
    for j in range(m - 1):
        numer, denom = 0.0, 0.0
        for i in range(n - j - 1):
            if not np.isnan(C[i, j]) and not np.isnan(C[i, j+1]):
                numer += C[i, j+1]
                denom += C[i, j]
        f_j = numer / denom if denom > 0 else 1.0
        f.append(f_j)
    f = np.array(f)

    # Step 3: Forecast triangle
    C_hat = C.copy()
    is_forecast = np.zeros_like(C, dtype=bool)
    for i in range(n):
        for j in range(m):
            if np.isnan(C_hat[i, j]):
                prev = C_hat[i, j - 1]
                factor = f[j - 1] if j - 1 < len(f) else 1.0
                C_hat[i, j] = prev * factor
                is_forecast[i, j] = True

    # Step 4: Estimate sigma^2_j
    sigma2 = []
    for j in range(m - 1):
        sum_sq, count = 0.0, 0
        for i in range(n - j - 1):
            if not np.isnan(C[i, j]) and not np.isnan(C[i, j+1]):
                ratio = C[i, j+1] / C[i, j]
                sum_sq += C[i, j] * (ratio - f[j]) ** 2
                count += 1
        sigma2_j = sum_sq / (count - 1) if count > 1 else 0.0
        sigma2.append(sigma2_j)

    # Step 5: Compute standard error for forecast
    std_error = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            if not np.isnan(C[i, j]):
                continue  # 已知数据，无误差
            var = 0.0
            prod = 1.0  # 累积乘积起始为1
            for k in range(j - 1, m - 1):
                if i + k - j + 1 >= n or k >= len(sigma2):
                    break
                var += sigma2[k] * (prod ** 2)
                prod *= f[k]  # 更新乘积
            std_error[i, j] = C_hat[i, j - 1] * np.sqrt(var)


    # Step 6: Save cumulative triangle
    pd.DataFrame(C_hat, index=origin_periods, columns=dev_periods).to_csv(output_path_triangle)

    # Step 7: Create long format output
    long_data = []
    total_reserve, total_var = 0.0, 0.0
    for i in range(n):
        for j in range(m):
            actual = C[i, j] if not np.isnan(C[i, j]) else None
            pred = C_hat[i, j]
            se = std_error[i, j] if is_forecast[i, j] else 0.0
            fit_err = pred - actual if actual is not None and not is_forecast[i, j] else None
            if is_forecast[i, j]:
                total_reserve += pred
                total_var += se ** 2
            long_data.append({
                "accident_month": origin_periods[i],
                "dev": dev_periods[j],
                "actual": actual,
                "predicted": pred,
                "std_error": se,
                "fit_error": fit_err,
                "is_forecast": is_forecast[i, j]
            })
    pd.DataFrame(long_data).to_csv(output_path_long, index=False)

    # Step 8: Output reserve estimate
    std_total = np.sqrt(total_var)
    lower, upper = total_reserve - 1.96 * std_total, total_reserve + 1.96 * std_total
    print("✅ Mack model run completed.")
    print(f"➡️  Total Reserve Estimate: {total_reserve:,.2f}")
    print(f"   95% Confidence Interval: [{lower:,.2f}, {upper:,.2f}]")
