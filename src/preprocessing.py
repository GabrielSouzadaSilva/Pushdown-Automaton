import re


class PreProcessing():

    def __init__(self, raw_dict):

        self.raw_comp = raw_dict["Components"]
        self.raw_rules = raw_dict["Rules"]

        self.components = self.get_dict_components()
        self.rules = self.get_rules()


    def get_dict_components(self) -> dict:

        components = dict()

        matches_for_comp = self.get_matches_components()

        for key in matches_for_comp.keys():
            components[key] = matches_for_comp[key][0]
            if key == "States":
                components["Initial State"] = matches_for_comp[key][1]
                components["Final States"] = matches_for_comp[key][2]

        for key, value in components.items():
            components[key] = self.format_str(value)

        components["Initial State"] = components["Initial State"][0]

        return components

    def get_matches_components(self) -> dict:

        symb_pattern = re.compile(r"{([a-z],\s*)*[a-z]}")
        state_pattern = re.compile(r"(q(\d+|f),\s*)*q(\d+|f)")
        stack_symb_pattern = re.compile(r"{([A-Z],\s*)*[A-Z]}")

        patterns = {"Symbols": symb_pattern, "States": state_pattern, "Stack Symbols": stack_symb_pattern}
        matches_comps = dict()

        for key, value in patterns.items():
            matches_comps[key] = self.find(value)

        return matches_comps

    def find(self, pattern) -> list:
        str_matches = []
        matches = re.finditer(pattern, self.raw_comp)
        for match in matches:
            str_matches.append(match.group())

        return str_matches

    def format_str(self, string) -> list:

        string = string.replace("{", "")
        string = string.replace("}", "")
        lista = string.split(",")

        for i in range(len(lista)):
            lista[i] = lista[i].strip()

        return lista

    def get_rules(self) -> list:

        rules = []
        dict_rules = dict()
        keys = ["origin_state", "word_read_symbol", "stack_read_symbol",
                "final_state", "stack_written_symbol"]

        for item in self.raw_rules:
            for i in range(5):
                dict_rules[keys[i]] = self.format_str(item)[i]
            rules.append(dict_rules)

        """
        rules = []

        for item in self.raw_rules:
            rules.append(self.format_str(item))
        """

        return rules