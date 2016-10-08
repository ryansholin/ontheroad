#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
#######################################################################################################

AUTHOR:             Adam Dynamic
CONTACT:            helloadamdynamic@gmail.com / www.adamdynamic.com
LAST REVISION:      14 December 2014

PROJECT:            War and Peace
DESCRIPTION:        Parses an input file of raw text and divides it intp sections no longer than
                    140 characters

#######################################################################################################
'''


import logging

from nltk import tokenize
import nltk.data
from nltk.tokenize import word_tokenize

def divide_sentence_by_brackets(input_string):
    '''
    :param input_string: A sentence input that is thought to contain a pair of brackets
    :return: A list of strings comprising of the sentence with the bracketed section as a seperate section
    '''

    FN_NAME = "divide_sentence_by_brackets"

    output = [input_string]

    try:

        while True:     # Continue the iteration until the final section does not contain a pair of brackets or an error is thrown

            temp_string = output[-1]

            # Check that the number of opening and closing brackets are the same
            number_of_opening_brackets = temp_string.count("(")
            number_of_closing_brackets = temp_string.count(")")

            if number_of_opening_brackets == number_of_closing_brackets:

                # Check that the file contains brackets, otherwise ignore and finish
                if number_of_opening_brackets > 0:

                    # Determine the position of both the opening and closing brackets
                    opening_bracket = temp_string.find("(")
                    closing_bracket = temp_string.find(")")

                    # Determine if the closing bracket is followed by punctuation, in which case include it in the section
                    if not closing_bracket + 1 == len(temp_string): # Check that the closing bracket isn't the last character
                        if not temp_string[closing_bracket + 1].isalpha():
                            closing_bracket = closing_bracket + 1

                    # Split the sentence and append to the end of the output
                    section_before_brackets = temp_string[0:opening_bracket].strip()

                    section_with_brackets = temp_string[opening_bracket:closing_bracket + 1].strip()
                    section_with_brackets = section_with_brackets[0] + section_with_brackets[1:].strip()   # Remove any spaces that follow the opening bracket

                    section_after_brackets = temp_string[closing_bracket + 1:].strip()

                    # Replace the last section in the list with the newly divided section
                    output = output[:len(output) - 1] + [section_before_brackets]
                    output.append(section_with_brackets)
                    output.append(section_after_brackets)

                else:
                    # Final section of the sentence does not contain any bracketed sections so the process is finished
                    break

            else:
                print input_string
                raise ValueError("Input string does not contain equal number of opening and closing brackets")

    except Exception, e:

        logging.error('%s Unable to divide sentence into sections split by brackets', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        # Remove the last item if it is blank
        if output[-1] == "":
            output.pop()

        return output


def divide_sentence_by_hyphens(input_string):
    '''
    :param input_string: A sentence input that is thought to contain a section seperated by hyphens
    :return: A list of strings comprising of the sentence with the hyphenated section as a seperate section
    '''

    FN_NAME = "divide_sentence_by_hyphens"

    output = [input_string]

    try:

        while True:     # Continue the iteration until the final section does not contain a pair of brackets or an error is thrown

            temp_string = output[-1]

            number_of_hyphens = temp_string.count("--")

            if number_of_hyphens >= 2:

                first_hyphen = temp_string.find("--")
                second_hyphen = temp_string.find("--", first_hyphen + 1)

                section_before_hyphens = temp_string[:first_hyphen].strip()
                section_with_hyphens = temp_string[first_hyphen:second_hyphen + 2].strip()
                section_after_hyphens = temp_string[second_hyphen + 2:].strip()

                # Replace the last section in the list with the newly divided section
                output = output[:len(output) - 1] + [section_before_hyphens]
                output.append(section_with_hyphens)
                output.append(section_after_hyphens)

            else:
                # Section does not contain a pair of hyphens and the process is complete
                break

    except Exception, e:

        logging.error('%s Unable to divide sentence into sections split by hyphens', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        # Remove the last item if it is blank
        if output[-1] == "":
            output.pop()

        return output


def split_using_nltk(input_string):
    '''
    :param input_string: A sentence input from the story
    :return: A list of strings divided using the NLTK algorithm
    '''

    # Split the sentence into tokens using the NLTK took kit
    split_lines = tokenize.sent_tokenize(input_string)

    output = recombine_split_quotations(split_lines)

    return output


def recombine_split_quotations(input_list):
    '''
    :param input_string: list of strings containing segments of text
    :return: a list of strings where quotation marks followed by a lower case letter are re-combined
    '''

    # e.g. ["This is the sentence," , " said the person"] becomes ["This is the sentence," said the person"]
    output = []
    temp_input = input_list[:]

    while temp_input:

        # If there is only one element of the input, then append it and break out of the loop
        if len(temp_input) == 1:
            output.append(temp_input[0])
            temp_input = []
            break

        # Else if there are two or more elements in the list:
        if temp_input[0][-1] == chr(34):

            if temp_input[1][0].strip().islower():

                temp_string = temp_input[0].strip() + " " + temp_input[1].strip()
                output.append(temp_string)
                temp_input = temp_input[2:]

            else:
                output.append(temp_input[0])
                temp_input = temp_input[1:]

        else:
            output.append(temp_input[0])
            temp_input = temp_input[1:]

    return output


def divide_sentence_by_puncutation(input_string, split_punctuation):
    '''
    :param input_string: A sentence input that is thought to contain a section seperated by punctuation
    :param split_punctuation: The punctuation that will be used to sub-divide the sentnence
    :return: A list of strings each ends with the split_punctuation character
    '''

    FN_NAME = "divide_sentence_by_punctuation"

    output = []

    try:

        if split_punctuation in input_string:

            # Get all the positions of the punctuation in the input string
            # Can't use input_string.split() because I need to capture the quotation marks
            punctuation_positions = [i for i, ltr in enumerate(input_string) if ltr == split_punctuation]

            # Check whether the following character is a quotation mark, and if so include it.
            for i in punctuation_positions:
                if len(input_string) > i + 1:
                    if input_string[i + 1] == chr(34):
                        punctuation_positions[punctuation_positions.index(i)] = i + 1

            if len(punctuation_positions) > 0:

                # Append the first section of the sentence to the output list
                output.append(input_string[:punctuation_positions[0] + 1].strip())

                for i in range(0, len(punctuation_positions) - 1):

                    temp_string = input_string[punctuation_positions[i]+1:punctuation_positions[i+1]+1]

                    output.append(temp_string.strip())

                # Append the final section of the sentence to the end
                output.append(input_string[punctuation_positions[-1] + 1:].strip())

        else:
            # If the split punctuation is not in the input string, just return the whole string
            output.append(input_string)

    except Exception, e:

        logging.error('%s Unable to divide sentence into sections split by the input punctuation', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        if output[-1] == "":
            output = output[:-1]
        return output


def split_nouns_and_commas(input_text):
    '''
    :param input_text: text to be split into segments
    :return: a list of sentences, split by nouns followed by commas
    '''

    FN_NAME = "split_nouns_with_commas"

    try:

        text = word_tokenize(input_text)
        split_sentence = nltk.pos_tag(text)

        nouns_with_commas = []
        output_list = []

        # Identify all of the nouns that are immediately followed by a comma
        for i in range(0, len(split_sentence) - 1):

            if split_sentence[i][1] == 'NN':
                if split_sentence[i+1][0] == "," and (split_sentence[i+2][0]==chr(34) or split_sentence[i+2][0]== chr(39)):
                    nouns_with_commas.append(i+2)

                elif split_sentence[i+1][0] == ",":
                    nouns_with_commas.append(i+1)

        # Create the sentence segments
        if len(nouns_with_commas) >= 1:

            for j in range(0, len(nouns_with_commas) + 1):

                start_position = 0
                end_position = len(input_text)
                output = ""

                # Identify the start and end points of each slice based on the split points identified
                if j == 0:
                    end_position = nouns_with_commas[0] + 1
                elif j == len(nouns_with_commas):               # i,e.if the comma the last in the list
                    start_position = nouns_with_commas[-1] + 1
                else:
                    start_position = nouns_with_commas[j-1] + 1
                    end_position = nouns_with_commas[j] + 1

                # Create an ordered list of words based on the split points
                sentence_segment = [word[0] for word in split_sentence[start_position:end_position]]

                # Join the sentence together based on
                for word in sentence_segment:
                    if word.isalnum() or word == "--":
                        output = output.strip() + " " + word
                    else:
                        output = output.strip() + word

                output_list.append(output)

        else:

            output_list = [input_text]

    except Exception, e:

        logging.error('%s Unable to split text by "nouns with commas"', FN_NAME)
        logging.exception('Traceback message: \n%s',e)
        print split_sentence
        print nouns_with_commas

        output_list = []

    finally:

        return output_list

def consolidate_sentence(input_list):
    '''
    :param input_list: A list of sentence segments split by punctuation
    :return: The same sentences, recombined where possible to maximise the length of each sentence
    '''

    FN_NAME = "consolidate_sentence"

    temp_list = input_list[:]

    try:

        number_of_iterations = len(input_list)
        j = 0

        # Iterate until all of the segments are shorter than 138 characters
        while j < number_of_iterations:

            if len(temp_list) == 1:
                break   # Can't consolidate a list of length one

            # Identify the smallest segment in the input_list
            list_of_sentence_lengths = [len(i) for i in temp_list]

            # Create a list of the indexes of the minumum sentence lengths in the temp_list
            min_sentence_positions = [i for i, x in enumerate(list_of_sentence_lengths) if x == min(list_of_sentence_lengths)]

            if min(min_sentence_positions) > 138:
                break   # The minimum sentence segment is already too long to be concatenated

            ### Doesn't capture the case where the first section can't be concatenated but a segment of equal min length elsewhere can be?
            sentence_index = min_sentence_positions[0]

            if sentence_index == 0:                     # If the minimum sentence is the first section, there is no left-hand section to test

                # Concatenate the strings if their total length is sufficiently short
                if len(temp_list[0]) + len(temp_list[1]) < 138:
                    temp_string = temp_list[0].strip() + " " + temp_list[1].strip()
                    temp_list = [temp_string] + temp_list[2:]

            elif sentence_index == len(temp_list) - 1:  # The test sentence is the last sentence, there is no right-hand section to test

                if len(temp_list[-1]) + len(temp_list[-2]) < 138:
                    temp_string = temp_list[-2].strip() + " " + temp_list[-1]
                    temp_list = temp_list[:-2] + [temp_string]

            else:
                adjacent_sentence_left = len(temp_list[sentence_index - 1])
                adjacent_sentence_right = len(temp_list[sentence_index + 1])

                if adjacent_sentence_left < adjacent_sentence_right:

                    if len(temp_list[sentence_index -1]) + len(temp_list[sentence_index]) < 138:
                        temp_string = temp_list[sentence_index - 1].strip() + " " + temp_list[sentence_index].strip()
                        temp_list = temp_list[:sentence_index - 1] + [temp_string] + temp_list[sentence_index + 1:]

                else:

                    if len(temp_list[sentence_index]) + len(temp_list[sentence_index + 1]) < 138:
                        temp_string = temp_list[sentence_index].strip() + " " + temp_list[sentence_index + 1].strip()
                        temp_list = temp_list[:sentence_index] + [temp_string] + temp_list[sentence_index + 2:]


            j = j + 1

    except Exception, e:

        logging.error('%s Unable to consolidate input sentence into <138 length sections', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        return temp_list


def close_quotation_marks(input_list):
    '''
    :param input_list: a list of strings containing the consolidated text of the paragraph
    :return: a list of strings where quotation marks have been opened and closed in each individual string
    '''

    FN_NAME = "close_quotation_marks"

    temp_list = input_list[:]
    output = []

    try:

        # To check whether there are open quotation marks, determine whether the string contains an even number
        while temp_list:

            # chr(34) = "
            number_of_quotations = temp_list[0].count(chr(34))

            # Hack fix to solve issue of chr(34) being replaced with chr(96)
            #if temp_list[0][0] == chr(96):
             #   temp_list[0] = chr(34) + temp_list[0][3:]

            if number_of_quotations % 2 != 0:
                temp_list[0] = temp_list[0].strip() + chr(34)

                # Only append a quotation mark to the start of the sentence if one isn't already there
                if temp_list[1][0] != chr(34):
                    temp_list[1] = chr(34) + temp_list[1].strip()

            output.append(temp_list[0])
            temp_list = temp_list[1:]

    except Exception, e:

        logging.error('%s Unable to close quotation marks', FN_NAME)
        logging.exception('Traceback message: \n%s',e)
        print "temp_list"
        print temp_list

    finally:

        return output



def split_sentence(input_string):
    '''
    :param input_string: A sentence that requires reducing in size
    :return: A list of strings comprising of the sentence split into smaller sections
    '''

    FN_NAME = "split_sentence"

    output = [input_string]

    # The sentences are divided according to the following hierarchy:
    # 1) Full stops, question marks, exclamation marks (using NLTK)
    # 2) Semi-colons
    # 3) Colons
    # 4) Hyphens
    # 5) Brackets
    # 6) Commas

    try:

        # Set the sentence length to 138 in order to accommodate quotation marks where necessary

        # 1) Full stops etc
        for sub_string in output:
            if len(sub_string) >= 138:
                # Create the new sub-strings and insert them into the output list where the old sentence was
                temp_output = split_using_nltk(sub_string)
                string_position = output.index(sub_string)
                output = output[:string_position] + temp_output + output[string_position + 1:]


        # 2) Semi-colons
        for sub_string in output:
            if len(sub_string) >= 138:
                # Create the new sub-strings and insert them into the output list where the old sentence was
                temp_output = divide_sentence_by_puncutation(sub_string, ";")
                string_position = output.index(sub_string)
                output = output[:string_position] + temp_output + output[string_position + 1:]


        # 3) Colons
        for sub_string in output:
            if len(sub_string) >= 138:
                # Create the new sub-strings and insert them into the output list where the old sentence was
                temp_output = divide_sentence_by_puncutation(sub_string, ":")
                string_position = output.index(sub_string)
                output = output[:string_position] + temp_output + output[string_position + 1:]

        # 4) Hyphens
        for sub_string in output:
            if len(sub_string) >= 138:
                temp_output = divide_sentence_by_hyphens(sub_string)
                string_position = output.index(sub_string)
                output = output[:string_position] + temp_output + output[string_position + 1:]

        # 5) Brackets
        for sub_string in output:
            if len(sub_string) >= 138:
                temp_output = divide_sentence_by_brackets(sub_string)
                string_position = output.index(sub_string)
                output = output[:string_position] + temp_output + output[string_position + 1:]


        # 5) #### Nouns with commas ###
        for sub_string in output:
            if len(sub_string) >= 138:
                temp_output = split_nouns_and_commas(sub_string)
                string_position = output.index(sub_string)
                output = output[:string_position] + temp_output + output[string_position + 1:]


        #6) Commas
        for sub_string in output:
            if len(sub_string) >= 138:
                # Create the new sub-strings and insert them into the output list where the old sentence was
                temp_output = divide_sentence_by_puncutation(sub_string, ",")
                string_position = output.index(sub_string)
                output = output[:string_position] + temp_output + output[string_position + 1:]


        output = consolidate_sentence(output)

        output = close_quotation_marks(output)

        # Add quotation marks where necessary

    except Exception, e:

        logging.error('%s Unable to split the input sentence', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:


        return output




def output_to_text_file(input_line):
    '''
    :param input_line: Line to enter into the output text file
    :return: nothing
    '''

    file_name = "otr_output.txt"

    # Append the new lines to the existing file
    file = open(file_name, "a")

    line_length = len(input_line)

    # If the line is longer than 140 characters, seperate using blank lines
    if line_length <= 140:
        file.write(input_line + "\n")

    else:
        file.write("\n")
        file.write(input_line + "\n")
        file.write("\n")

    file.close()


def import_text_file(text_file_location):
    '''
    :param text_file_location: The file location of the text file to import into the story database
    :return: nothing
    '''

    FN_NAME = "import_text_file"

    try:

        story = open(text_file_location, 'r')

        for line in story:

            if line != "":

                line = line.strip()

                # Divide the sentence into sections smaller than 140 characters
                output = split_sentence(line)

                if output != ['']:
                    print "Output"
                    print output
                    for output_line in output:

                        output_to_text_file(output_line)

    except Exception, e:

        logging.error('%s Unable to import text file', FN_NAME)
        logging.exception('Traceback message: \n%s',e)

    finally:

        print "Process complete"




import_text_file("otr_import.txt")
