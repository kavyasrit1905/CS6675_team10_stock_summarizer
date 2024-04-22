import matplotlib.pyplot as plt

# Your data
content_length = [3793, 9028, 1244, 2919, 1097, 5527, 288, 2730, 5707, 686, 2049, 2861, 3604, 2732, 2796, 5328, 2737, 2510, 2802, 2591, 2976, 2733, 2760, 4464, 1033, 2714, 2715, 1703, 1696, 1296]
times = [2.32, 3.42, 1.47, 2.52, 2.14, 3.91, 1.73, 3.12, 1.97, 2.73, 2.73, 3.85, 3.17, 3.97, 3.03, 3.82, 3.96, 2.24, 2.64, 3.92, 3.93, 2.98, 2.78, 2.73, 2.83, 2.02, 4.75, 1.67, 2.56, 7.76, 1.95]

# Plotting the graph
plt.figure(figsize=(12, 6))
plt.scatter(content_length, times, color='blue', label='Times')
plt.xlabel('Content Length')
plt.ylabel('Times')
plt.title('Content Length vs. Times')
plt.legend()
plt.grid(True)
plt.show()