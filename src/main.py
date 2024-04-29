from assessment import Assessment
from pathlib import Path
import os


if __name__ == "__main__":

    root_path = Path(__file__).parents[1]
    input_path = os.path.join(root_path, "input.txt")
    output_path = os.path.join(root_path, "output.txt")
    assessment = Assessment(input_path, output_path)
    assessment.run()
