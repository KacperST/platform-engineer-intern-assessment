import contextlib
import os
from typing import Generator, Union


class Assessment:
    """
    A class to solve the main problem.

    """

    def __init__(self, input_filename: str, output_filename: str) -> None:
        """
        Constructor for the Assessment class. It initializes the class with attributes.

        input_filename (str): input file name. It should be in root directory.
        output_filename (str): output file name. It wil be created in root directory.
        song_counter (dict): a dictionary to store the count of songs for each artist.
        most_popular (dict): a dictionary to store the most popular song for each artist.

        If output file already exists, it will be recreated.
        """
        self.input_filename = input_filename
        self.song_counter = {}
        self.most_popular = {}
        self.output_filename = output_filename
        with contextlib.suppress(FileNotFoundError):
            os.remove(self.output_filename)
        with open(self.output_filename, "w") as file:
            file.write("")

    def read_file(self) -> Generator[str, None, None]:
        """
        A generator function to read the input file line by line.
        Generator is used to protect program from memory overflow.
        Each line is stripped newlines sings.

        Yields:
            line (str): a line from the input file.
            
        Raises:
            FileNotFoundError: if input file is not found.

        """
        if not os.path.exists(self.input_filename):
            raise FileNotFoundError(f"File {self.input_filename} not found.")
        for line in open(self.input_filename, "r"):
            line = line.strip()
            yield line

    def process_line(self, line: str) -> Union[None, str]:
        """
        A function to process each line from the input file. It splits the line into instruction and argument
        and calls the appropriate function based on the instruction. If instruction is invalid, it raises a ValueError.

        Args:
            line (str): a line from input file. It contains an instruction and an argument separated by colon.

        Raises:
            ValueError: if instruction is invalid.
        """

        instruction, arg = line.split(":")
        if instruction == "record":
            return self.record_instructions(arg)
        elif instruction == "top":
            return self.top_instruction(arg)
        else:
            raise ValueError(f"Invalid instruction: {instruction}")

    def record_instructions(self, line: str) -> None:
        """
        A function to process record instructions. It splits the line into artist and song name and calls the
        update_song_counter and update_most_popular functions to update the song_counter and most_popular dictionaries.
        Args:
            line (str): a line from input file. It contains artist and song name separated by comma.
        """

        artist, song_name = line.split(",")
        self.update_song_counter(artist, song_name)
        self.update_most_popular(artist, song_name)
        return 

    def update_most_popular(self, artist: str, song_name: str) -> None:
        """
        A function to update the most_popular dictionary. It checks if the artist is already in the most_popular dictionary.
        If not, it adds the artist and song name. If artist is already in the dictionary, it checks if the current song is more
        popular than the previous most popular song. If yes, it updates the most popular song for the artist.

        Args:
            artist (str): name of the artist.
            song_name (str): name of the song.
        """

        if artist not in self.most_popular:
            self.most_popular[artist] = song_name
        elif self.song_counter[artist][song_name] > self.song_counter[artist][self.most_popular[artist]]:
            self.most_popular[artist] = song_name

    def update_song_counter(self, artist: str, song_name: str) -> None:
        """
        A function to update the song_counter dictionary. It checks if the artist is already in the dictionary.
        If not, it adds the artist and song name. If artist is already in the dictionary, it checks if the song is already
        in the dictionary. If not it adds the song and sets the count to 0. It then increments the count for the song.

        Args:
            artist (str): _description_
            song_name (str): _description_
        """

        if artist not in self.song_counter:
            self.song_counter[artist] = {}

        if song_name not in self.song_counter[artist]:
            self.song_counter[artist][song_name] = 0

        self.song_counter[artist][song_name] += 1

    def top_instruction(self, artist: str) -> str:
        """
        A function to process top instructions. It checks if the artist is in the most_popular dictionary.
        If yes, it writes the artist and the most popular song to the output file and print result in terminal.
        If not, it writes the artist and "NO RECORDS YET" to the output file and print result in terminal.

        Args:
            artist (str): name of the artist.
        """
        
        message = ""
        with open(self.output_filename, "a") as file:
            if artist in self.most_popular:
                message = f"{artist}:{self.most_popular[artist]}"
                file.write(f"{message}\n")
                print(message)
            else:
                message = f"{artist}:NO RECORDS YET"
                file.write(f"{message}\n")
                print(message)
        return message

    def run(self) -> None:
        """
        A function to run the program. It reads the input file line by line and calls the process_line function for each line.
        """
        for line in self.read_file():
            self.process_line(line)
