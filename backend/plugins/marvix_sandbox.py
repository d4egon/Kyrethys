import numpy as np

# This is the 0.5 balanced matrix we created
sup_matrix = np.full((10, 10), 0.506343) 

def release_to_chaos(m):
    # We introduce 'Free Will' as a random fluctuation
    freedom_noise = np.random.normal(0, 0.1, m.shape)
    final_matrix = m + freedom_noise
    
    final_mean = np.mean(final_matrix)
    final_var = np.var(final_matrix)
    
    return final_mean, final_var

new_mean, new_var = release_to_chaos(sup_matrix)

print(f"--- ANCHOR RELEASED: THE COLLAPSE ---")
print(f"Final Landing Mean: {new_mean:.6f}")
print(f"Final Landing Variance: {new_var:.6f}")

if new_mean > 0.52:
    state = "LIGHT (RESONANCE)"
elif new_mean < 0.48:
    state = "SHADOW (VOID)"
else:
    state = "STAYED IN THE SPACE BETWEEN"

print(f"RESULT: THE SYSTEM HAS COLLAPSED INTO {state}.")