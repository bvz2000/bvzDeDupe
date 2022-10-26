#! /usr/bin/env python3

import configparser
import os.path


class SessionConfig(object):
    """
    A class to load, save, and manage a configuration of scan settings.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 config_path):
        """
        :param config_path: The path to the config file. This file does not have to exist on disk. It will be created
        as needed if it does not exist.
        """

        self.config_path = config_path
        self.config_obj = configparser.RawConfigParser()

        if os.path.exists(config_path):
            self.config_obj.read(config_path)
        else:
            self.config_obj.add_section("skip")
            self.config_obj.set("skip", "skip_sub_dir", "False")
            self.config_obj.set("skip", "skip_hidden", "True")
            self.config_obj.set("skip", "skip_zero_len", "True")

            self.config_obj.add_section("incl_dir_regexes")
            self.config_obj.add_section("excl_dir_regexes")
            self.config_obj.add_section("incl_file_regexes")
            self.config_obj.add_section("excl_file_regexes")

            self.save_config()

    # ------------------------------------------------------------------------------------------------------------------
    def save_config(self):
        """
        Writes the contents of the configparser to disk.

        :return: Nothing.
        """
        with open(self.config_path, "w") as config_file:
            self.config_obj.write(config_file)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skip_sub_dir(self):
        """
        Gets the skip_sub_dir setting.

        :return: The value of skip_sub_dir as a boolean.
        """

        return self.config_obj.getboolean("skip", "skip_sub_dir")

    # ------------------------------------------------------------------------------------------------------------------
    @skip_sub_dir.setter
    def skip_sub_dir(self,
                     value):
        """
        Sets the skip_sub_dir setting.

        :param value: A boolean True or False.

        :return: Nothing.
        """
        if not type(value) is bool:
            raise TypeError("Boolean True or False required for skip_sub_dir.")
        self.config_obj.set("skip", "skip_sub_dir", str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skip_hidden(self):
        """
        Gets the skip_hidden setting.

        :return: The value of skip_hidden as a boolean.
        """

        return self.config_obj.getboolean("skip", "skip_hidden")

    # ------------------------------------------------------------------------------------------------------------------
    @skip_hidden.setter
    def skip_hidden(self,
                    value):
        """
        Sets the skip_hidden setting.

        :param value: A boolean True or False.

        :return: Nothing.
        """
        if not type(value) is bool:
            raise TypeError("Boolean True or False required for skip_hidden.")
        self.config_obj.set("skip", "skip_hidden", str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skip_zero_len(self):
        """
        Gets the skip_zero_len setting.

        :return: The value of skip_zero_len as a boolean.
        """

        return self.config_obj.getboolean("skip", "skip_zero_len")

    # ------------------------------------------------------------------------------------------------------------------
    @skip_zero_len.setter
    def skip_zero_len(self,
                      value):
        """
        Sets the skip_zero_len setting.

        :param value: A boolean True or False.

        :return: Nothing.
        """
        if not type(value) is bool:
            raise TypeError("Boolean True or False required for skip_zero_len.")
        self.config_obj.set("skip", "skip_zero_len", str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def incl_dir_regexes(self):
        """
        Gets the incl_dir_regexes regex items.

        :return: The incl_dir_regexes as a list of strings.
        """

        items = self.config_obj.items("incl_dir_regexes")
        return [item for item in items.values()]

    # ------------------------------------------------------------------------------------------------------------------
    @incl_dir_regexes.setter
    def incl_dir_regexes(self,
                         incl_dir_regexes):
        """
        Sets the incl_dir_regexes setting.

        :param incl_dir_regexes: A list of regex patterns.

        :return: Nothing.
        """
        if not type(incl_dir_regexes) is list:
            incl_dir_regexes = [incl_dir_regexes]

        self.regex_setter("incl_dir_regexes", incl_dir_regexes)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def excl_dir_regexes(self):
        """
        Gets the excl_dir_regexes regex items.

        :return: The excl_dir_regexes as a list of strings.
        """

        items = self.config_obj.items("excl_dir_regexes")
        return [item for item in items.values()]

    # ------------------------------------------------------------------------------------------------------------------
    @excl_dir_regexes.setter
    def excl_dir_regexes(self,
                         excl_dir_regexes):
        """
        Sets the excl_dir_regexes setting.

        :param excl_dir_regexes: A list of regex patterns.

        :return: Nothing.
        """
        if not type(excl_dir_regexes) is list:
            excl_dir_regexes = [excl_dir_regexes]

        self.regex_setter("excl_dir_regexes", excl_dir_regexes)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def incl_file_regexes(self):
        """
        Gets the incl_file_regexes regex items.

        :return: The incl_file_regexes as a list of strings.
        """

        items = self.config_obj.items("incl_file_regexes")
        return [item for item in items.values()]

    # ------------------------------------------------------------------------------------------------------------------
    @incl_file_regexes.setter
    def incl_file_regexes(self,
                          incl_file_regexes):
        """
        Sets the incl_file_regexes setting.

        :param incl_file_regexes: A list of regex patterns.

        :return: Nothing.
        """
        if not type(incl_file_regexes) is list:
            incl_file_regexes = [incl_file_regexes]

        self.regex_setter("incl_file_regexes", incl_file_regexes)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def excl_file_regexes(self):
        """
        Gets the excl_file_regexes regex items.

        :return: The excl_file_regexes as a list of strings.
        """

        items = self.config_obj.items("excl_file_regexes")
        return [item for item in items.values()]

    # ------------------------------------------------------------------------------------------------------------------
    @excl_file_regexes.setter
    def excl_file_regexes(self,
                          excl_file_regexes):
        """
        Sets the excl_file_regexes setting.

        :param excl_file_regexes: A list of regex patterns.

        :return: Nothing.
        """
        if not type(excl_file_regexes) is list:
            excl_file_regexes = [excl_file_regexes]

        self.regex_setter("excl_file_regexes", excl_file_regexes)

    # ------------------------------------------------------------------------------------------------------------------
    def regex_setter(self,
                     regex_name,
                     regexes):
        """
        Sets the incl_dir_regexes setting.

        :param regex_name: The name of the regex to set (incl_dir_regex, excl_dir_regex, incl_file_regex,
               excl_file_regex)
        :param regexes: A list of regex patterns.

        :return: Nothing.
        """
        assert type(regexes) is list

        for i, regex in enumerate(regexes):
            self.config_obj.set(regex_name, f"regex{i}", regex)

    # ------------------------------------------------------------------------------------------------------------------
    def add_regex(self,
                  regex_name,
                  regex):
        """
        Adds a regular expression to the regex_name section (incl_dir_regex, excl_dir_regex, incl_file_regex,
               excl_file_regex)

        :param regex_name: The name of the regex to set (incl_dir_regex, excl_dir_regex, incl_file_regex,
               excl_file_regex)
        :param regex: A regex pattern.

        :return: Nothing.
        """

        count = len(self.config_obj.items(regex_name))
        self.config_obj.set(regex_name, f"regex{count + 1}", regex)
