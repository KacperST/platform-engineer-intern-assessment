import contextlib
from src.assessment import Assessment
from unittest.mock import patch, mock_open

import os
import pytest

@pytest.fixture(autouse=True)
def prepare_and_clean_output_file():
    with contextlib.suppress(FileNotFoundError):
        os.remove("tests/output.txt")
    yield
    with contextlib.suppress(FileNotFoundError):
        os.remove("tests/output.txt")   

@pytest.fixture
def input_filename():
    return "tests/input.txt"

@pytest.fixture
def output_filename():
    return "tests/output.txt"

@pytest.fixture
def random_output():
    if not os.path.exists("tests/output.txt"):
        with open("tests/output.txt", "w") as file:
            file.write("SOME RANDOM DATA")
    return 

@pytest.fixture
def wrong_input_filename():
    return "tests/wrong_input.txt"

@pytest.fixture
def record_instruction():
    return "record:Taylor Swift,Cruel Summer"


@pytest.fixture
def top_instruction():
    return "top:Taylor Swift"

@pytest.fixture
def wrong_instruction():
    return "wrong:Taylor Swift"

@pytest.fixture
def record_row():
    return "Taylor Swift,Cruel Summer"

@pytest.fixture
def record_second_row():
    return "Taylor Swift,Blank Space"

@pytest.fixture
def output_from_readme():
    return "Taylor Swift:Cruel Summer\nMichael Jackson:Beat it\n"

class TestAssessment:
    
            
    def test_init_attributes(self, input_filename, output_filename, random_output):
        assessment = Assessment(input_filename, output_filename)
        assert assessment.input_filename == "tests/input.txt"
        assert assessment.song_counter == {}
        assert assessment.most_popular == {}
        assert assessment.output_filename == "tests/output.txt"
        
    def test_if_init_recreates_output_file(self, input_filename, output_filename, random_output):
        Assessment(input_filename, output_filename)
        assert os.path.exists(output_filename)
        with open(output_filename, "r") as file:
            assert file.read() == ""
            
    def test_read_file_wrong_input_filename(self, wrong_input_filename, output_filename, random_output):
        assessment = Assessment(wrong_input_filename, output_filename)
        with pytest.raises(FileNotFoundError):
            next(assessment.read_file())
            
    def test_read_file(self, input_filename, output_filename):
        assessment = Assessment(input_filename, output_filename)
        assert next(assessment.read_file()) == "record:Taylor Swift,Cruel Summer"
        
    def test_process_line(self, input_filename, output_filename, record_instruction, top_instruction, wrong_instruction):
        assessment = Assessment(input_filename, output_filename)
        record_output = assessment.process_line(record_instruction)
        assert record_output == None
        with patch.object(Assessment, 'top_instruction', return_value="Taylor Swift:Cruel Summer"):
            top_output = assessment.process_line(top_instruction)
            assert top_output == "Taylor Swift:Cruel Summer"
        with pytest.raises(ValueError):
            assessment.process_line(wrong_instruction)
            
    def test_record_instructions(self, input_filename, output_filename, record_row):
        assessment = Assessment(input_filename, output_filename)
        result = assessment.record_instructions(record_row)
        assert result == None
        assert assessment.song_counter == {"Taylor Swift": {"Cruel Summer": 1}}
        assert assessment.most_popular == {"Taylor Swift": "Cruel Summer"}
        
    def test_update_song_counter(self, input_filename, output_filename, record_row, record_second_row):
        assessment = Assessment(input_filename, output_filename)
        artist1, song1 = record_row.split(",")
        assert assessment.song_counter == {}
        assessment.update_song_counter(artist1, song1)
        assert assessment.song_counter == {"Taylor Swift": {"Cruel Summer": 1}}
        assessment.update_song_counter(artist1, song1)
        assert assessment.song_counter == {"Taylor Swift": {"Cruel Summer": 2}}
    
    def test_update_most_popular(self, input_filename, output_filename, record_row, record_second_row):
        assessment = Assessment(input_filename, output_filename)
        artist1, song1 = record_row.split(",")
        assert assessment.most_popular == {}
        assert assessment.update_song_counter(artist1, song1) == None
        assessment.update_most_popular(artist1, song1)
        assert assessment.most_popular == {"Taylor Swift": "Cruel Summer"}
        artist1, song2 = record_second_row.split(",")
        assessment.update_song_counter(artist1, song2)
        assessment.update_most_popular(artist1, song2)
        assessment.update_song_counter(artist1, song2)
        assessment.update_most_popular(artist1, song2)
        assert assessment.most_popular == {"Taylor Swift": "Blank Space"}
        
    def test_top_instruction(self, input_filename, output_filename):
        assessment = Assessment(input_filename, output_filename)
        assessment.most_popular = {"Taylor Swift": "Cruel Summer"}
        assert assessment.top_instruction("Taylor Swift") == "Taylor Swift:Cruel Summer"
        assert assessment.top_instruction("Adele") == "Adele:NO RECORDS YET"       
        
    def test_run(self, input_filename, output_filename):
        assessment = Assessment(input_filename, output_filename)
        with patch.object(Assessment, 'process_line', return_value=None) as mock_method:
            assessment.run()
            mock_method.assert_called()

    def test_end_to_end_from_readme(self, input_filename, output_filename, output_from_readme):
        assessment = Assessment(input_filename, output_filename)
        assessment.run()
        with open("tests/output.txt", "r") as file:
            assert file.read() == output_from_readme
        