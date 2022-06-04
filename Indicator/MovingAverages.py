def moving_average(data: list[float], time_period: int) -> list[float]:
    if not time_period < len(data):
        raise ValueError("Moving average time period is longer than the list of data")

    if len(data) == 0:
        return []

    averages = [data[0]]
    for i in range(1, len(data)):
        if i < time_period:
            average = sum(data[:i]) / i
        else:
            average = sum(data[i-time_period:i]) / time_period

        averages.append(average)
    return averages