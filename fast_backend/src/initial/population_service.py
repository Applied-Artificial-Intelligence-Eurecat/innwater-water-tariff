from src.initial.schemas import PopulationModel
import matplotlib.pyplot as plt
import io
import base64


async def generate_population_plot(input_data: PopulationModel) -> io.BytesIO:
    """
    Generate a population plot based on the input data.

    Args:
        input_data: The population model containing the input parameters

    Returns:
        dict: Base64 encoded image and content type
    """
    # Your logic code goes here using input_data parameters
    # Example implementation (replace with your actual logic)
    buf = await mock_data()
    return buf


async def mock_data():
    x_values = [1, 2, 3, 4, 5]
    y_values = [10, 20, 30, 40, 50]
    # Create the plot
    fig, axs = plt.subplots(1, 1, figsize=(10, 6))
    axs.scatter(x_values, y_values)
    # Add titles and labels
    axs.set_title("Population Plot")
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
