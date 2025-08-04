import io

from matplotlib import pyplot as plt

from src.core.models import Simulation


async def mock_data(title: str):
    x_values = [1, 2, 3, 4, 5]
    y_values = [10, 20, 30, 40, 50]
    # Create the plot
    fig, axs = plt.subplots(1, 1, figsize=(10, 6))
    axs.scatter(x_values, y_values)
    # Add titles and labels
    axs.set_title(title)
    axs.set_xlabel("Years")
    axs.set_ylabel("Population")
    # Add grid for better readability
    axs.grid(True, linestyle='--', alpha=0.7)
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


async def generate_tbse_par_affordability_plot(simulation: Simulation) -> io.BytesIO:
    return await mock_data("TBSE Par Affordability Plot")


async def generate_tbse_consumption_plot(simulation: Simulation) -> io.BytesIO:
    return await mock_data("TBSE Consumption Plot")


async def generate_pens_parade_consumptions_plot(simulation: Simulation) -> io.BytesIO:
    return await mock_data("Pen's Parade Consumptions Plot")


async def generate_consumption_deviation_losses_cost_recovery_plot(simulation: Simulation) -> io.BytesIO:
    return await mock_data("Consumption Deviation Losses Cost Recovery Plot")
