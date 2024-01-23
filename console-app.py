import npyscreen
from social_graph_tool.connection_graph import (
    ConnectionGraph,
    import_graph_from_graphml_file,
    export_graph_to_graphml_file,
)


class MainMenu(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edited = False
        self.graph_name = None
        self.connection_graph = None

    def beforeEditing(self):
        if self.connection_graph:
            self.name = f"Social Graph Tool - Main Menu ({self.graph_name} - {len(self.connection_graph.nodes)} nodes, {len(self.connection_graph.edges)} edges)"
        else:
            self.name = "Social Graph Tool - Main Menu (No Graph Loaded)"

    def create(self):
        self.menu_value = self.add(
            MainMenuSelector,
            scroll_exit=True,
            max_height=9,
            name="Main Menu Options",
            values=[
                "New Graph",
                "Load Graph",
                "Clear Graph",
                "Add Person",
                "Add Node",
                "Add Edge",
                "Search",
                "Save Graph",
                "Exit",
            ],
        )


class MainMenuSelector(npyscreen.MultiLineAction):
    def _select_next_form(self, act_on_this, key_press):
        if act_on_this == "New Graph":  # Destructive
            self._handle_destructive_action("NEWGRAPH")
        elif act_on_this == "Load Graph":  # Destructive
            self._handle_destructive_action("LOADGRAPH")
        elif act_on_this == "Clear Graph":  # Destructive
            self.parent.parentApp.getForm("MAIN").connection_graph = None
            self.parent.parentApp.getForm("MAIN").graph_name = None
            self.parent.parentApp.getForm("MAIN").edited = False
            self.parent.parentApp.switchForm("MAIN")
        elif act_on_this == "Add Person":
            self._fail_if_no_graph("ADDPERSON")
        elif act_on_this == "Add Node":
            self._fail_if_no_graph("ADDNODECHOICE")
        elif act_on_this == "Add Edge":
            self._fail_if_no_graph("ADDEDGECHOICE")
        elif act_on_this == "Search":
            self._fail_if_no_graph("SKILLSEARCH")
        elif act_on_this == "Save Graph":
            self.parent.parentApp.getForm("SAVEGRAPH").next_form = "MAIN"
            self._fail_if_no_graph("SAVEGRAPH")
        elif act_on_this == "Exit":  # Destructive
            self._handle_destructive_action(None)

    def _handle_destructive_action(self, next_form):
        if self.parent.parentApp.getForm("MAIN").edited:
            self.parent.parentApp.getForm("OVERWRITE").next_form = next_form
            self.parent.parentApp.switchForm("OVERWRITE")
        else:
            self.parent.parentApp.switchForm(next_form)

    def _fail_if_no_graph(self, form_for_success):
        curr_graph = self.parent.parentApp.getForm("MAIN").connection_graph
        if not curr_graph:
            npyscreen.notify_confirm("No open graph!", title="Error")
            self.parent.parentApp.switchForm("MAIN")
        else:
            self.parent.parentApp.switchForm(form_for_success)

    def actionHighlighted(self, act_on_this, key_press):
        self._select_next_form(act_on_this, key_press)


class OverwriteGraph(npyscreen.Form):
    def init(self):
        self.next_form = None

    def create(self):
        self.save_first = self.add(
            npyscreen.TitleSelectOne,
            max_height=4,
            name="This action is destructive. Save working graph?",
            values=["Yes", "No"],
        )

    def afterEditing(self):
        if self.save_first.value[0] == 0:
            self.parentApp.getForm("SAVEGRAPH").next_form = self.next_form
            self.parentApp.setNextForm("SAVEGRAPH")
        else:
            self.parentApp.setNextForm(self.next_form)


class AddNodeChoice(npyscreen.Form):
    def create(self):
        self.menu_value = self.add(
            NodeSelector,
            scroll_exit=True,
            max_height=8,
            name="Choose Node Type to Add:",
            values=[
                "PERSON",
                "PLACE",
                "ORGANIZATION",
                "ACCOUNT",
                "Back to Main Menu",
            ],
        )


class NodeSelector(npyscreen.MultiLineAction):
    def _select_next_form(self, act_on_this, key_press):
        if act_on_this == "PERSON":
            self.parent.parentApp.switchForm("ADDPERSON")
        elif act_on_this == "PLACE":
            self.parent.parentApp.getForm("ADDNODECHOICE").node_choice = "PLACE"
            self.parent.parentApp.switchForm("ADDNODE")
        elif act_on_this == "ORGANIZATION":
            self.parent.parentApp.getForm("ADDNODECHOICE").node_choice = "ORGANIZATION"
            self.parent.parentApp.switchForm("ADDNODE")
        elif act_on_this == "ACCOUNT":
            self.parent.parentApp.getForm("ADDNODECHOICE").node_choice = "ACCOUNT"
            self.parent.parentApp.switchForm("ADDNODE")
        elif act_on_this == "Back to Main Menu":
            self.parent.parentApp.switchForm("MAIN")

    def actionHighlighted(self, act_on_this, key_press):
        self._select_next_form(act_on_this, key_press)


class AddNode(npyscreen.Form):
    def beforeEditing(self):
        self.node_choice = self.parentApp.getForm("ADDNODECHOICE").node_choice
        self.name = f"Social Graph Tool - Add Node ({self.node_choice})"

    def create(self):
        self.label = self.add(npyscreen.TitleText, name="Label:")

    def afterEditing(self):
        if self.label.value:
            self.parentApp.getForm("MAIN").connection_graph.add_node(
                self.label.value, kind=self.node_choice
            )
            self.parentApp.getForm("MAIN").edited = True
        else:
            npyscreen.notify_confirm("No label provided!", title="Error")
        self.parentApp.setNextForm("MAIN")


class AddEdgeChoice(npyscreen.Form):
    def create(self):
        self.menu_value = self.add(
            EdgeSelector,
            scroll_exit=True,
            max_height=8,
            name="Choose Edge Type to Add (Note: Person must exist, but dest will be created if not):",
            values=[
                "ASSOCWITH(Person, Oranization)",
                "ONACCOUNT(Person, Account)",
                "BASEDIN(Person, Place)",
                "Back to Main Menu",
            ],
        )


class EdgeSelector(npyscreen.MultiLineAction):
    def _select_next_form(self, act_on_this, key_press):
        self.parent.parentApp.getForm("ADDEDGECHOICE").edge_title = act_on_this
        if act_on_this == "ASSOCWITH(Person, Oranization)":
            self.parent.parentApp.getForm("ADDEDGECHOICE").edge_choice = "ASSOCWITH"
            self.parent.parentApp.switchForm("ADDEDGE")
        elif act_on_this == "ONACCOUNT(Person, Account)":
            self.parent.parentApp.getForm("ADDEDGECHOICE").edge_choice = "ONACCOUNT"
            self.parent.parentApp.switchForm("ADDEDGE")
        elif act_on_this == "BASEDIN(Person, Place)":
            self.parent.parentApp.getForm("ADDEDGECHOICE").edge_choice = "BASEDIN"
            self.parent.parentApp.switchForm("ADDEDGE")
        elif act_on_this == "Back to Main Menu":
            self.parent.parentApp.switchForm("MAIN")

    def actionHighlighted(self, act_on_this, key_press):
        self._select_next_form(act_on_this, key_press)


class AddEdge(npyscreen.Form):
    def beforeEditing(self):
        self.edge_choice = self.parentApp.getForm("ADDEDGECHOICE").edge_choice
        self.edge_title = self.parentApp.getForm("ADDEDGECHOICE").edge_title
        self.name = f"Social Graph Tool - Add Edge ({self.edge_title})"

    def create(self):
        self.source = self.add(npyscreen.TitleText, name="Source:")
        self.dest = self.add(npyscreen.TitleText, name="Endpoint:")

    def afterEditing(self):
        if self.edge_choice == "ASSOCWITH":
            self.parentApp.getForm("MAIN").connection_graph.add_person_org_edge(
                self.source.value, self.dest.value
            )
            self.parentApp.getForm("MAIN").edited = True
        elif self.edge_choice == "ONACCOUNT":
            self.parentApp.getForm("MAIN").connection_graph.add_person_account_edge(
                self.source.value, self.dest.value
            )
            self.parentApp.getForm("MAIN").edited = True
        elif self.edge_choice == "BASEDIN":
            self.parentApp.getForm("MAIN").connection_graph.add_person_place_edge(
                self.source.value, self.dest.value
            )
            self.parentApp.getForm("MAIN").edited = True
        else:
            npyscreen.notify_confirm("No edge choice selected!", title="Error")
        self.parentApp.setNextForm("MAIN")


class LoadGraph(npyscreen.Form):
    def create(self):
        self.graph_name = self.add(
            npyscreen.TitleText,
            name="Graph Name:",
        )
        self.input_graph_file = self.add(
            npyscreen.TitleFilenameCombo,
            name="Graph File:",
        )

    def afterEditing(self):
        try:
            g = import_graph_from_graphml_file(self.input_graph_file.value)
            self.parentApp.getForm("MAIN").connection_graph = g
            self.parentApp.getForm("MAIN").graph_name = self.graph_name.value
        except FileNotFoundError:
            npyscreen.notify_confirm(
                f"File {self.input_graph_file.value} not found!", title="Error"
            )
        self.parentApp.setNextForm("MAIN")


class NewGraph(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.getForm("MAIN").connection_graph = ConnectionGraph()
        self.parentApp.getForm("MAIN").graph_name = self.graph_name.value
        self.parentApp.getForm("MAIN").edited = True
        self.parentApp.setNextForm("MAIN")

    def create(self):
        self.graph_name = self.add(
            npyscreen.TitleText, name="New Graph Name:", begin_entry_at=20
        )


class SaveGraph(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_form = "MAIN"

    def beforeEditing(self):
        curr_graph = self.parentApp.getForm("MAIN").connection_graph
        if not curr_graph:
            npyscreen.notify_confirm("No open graph to save!", title="Error")
            self.parentApp.setNextForm(self.next_form)

    def create(self):
        self.save_file = self.add(
            npyscreen.TitleText, name="Save File Name:", begin_entry_at=20
        )

    def afterEditing(self):
        export_graph_to_graphml_file(
            self.parentApp.getForm("MAIN").connection_graph, self.save_file.value
        )
        self.parentApp.getForm("MAIN").edited = False
        self.parentApp.setNextForm(self.next_form)


class AddPerson(npyscreen.Form):
    def create(self):
        self.person_name = self.add(
            npyscreen.TitleText, name="Person Name:", begin_entry_at=24
        )
        self.person_role = self.add(
            npyscreen.TitleText, name="Person Role:", begin_entry_at=24
        )
        self.person_place = self.add(
            npyscreen.TitleText, name="Person Place:", begin_entry_at=24
        )
        self.person_org = self.add(
            npyscreen.TitleText, name="Person Org:", begin_entry_at=24
        )
        self.person_account = self.add(
            npyscreen.TitleText, name="Person Account:", begin_entry_at=24
        )
        self.person_skills = self.add(
            npyscreen.TitleText, name="Person Skills (CSV):", begin_entry_at=24
        )
        self.person_nodes = self.add(
            npyscreen.TitleText, name="Person Notes (CSV):", begin_entry_at=24
        )

    def afterEditing(self):
        if self.person_name.value:
            curr_graph = self.parentApp.getForm("MAIN").connection_graph
            curr_graph.add_person(
                self.person_name.value,
                role=self.person_role.value,
                place=self.person_place.value,
                org=self.person_org.value,
                account=self.person_account.value,
                skills=self.person_skills.value,
                notes=self.person_nodes.value,
            )
            self.parentApp.getForm("MAIN").edited = True
        else:
            npyscreen.notify_confirm("No person name provided!", title="Error")
        self.parentApp.setNextForm("MAIN")


class SkillSearch(npyscreen.Form):
    def create(self):
        self.query = self.add(
            npyscreen.TitleText,
            name="Skill Query:",
        )

    def _tabulate_results(self, node_results, additional_data):
        sorted_results = dict(
            sorted(node_results.items(), key=lambda item: item[1]["label"])
        )
        out = f'{"NAME":<30}{"ROLE":<50}{"LOCATION":<30}{"ORGANIZATION":<50}{"ACCOUNT":<30}{"SKILLS"}\n'
        out += f"{'='*200}\n"
        for key, value in sorted_results.items():
            if "role" not in value:
                value["role"] = ""
            tmp_data = additional_data[key]
            place_str, org_str, account_str = "", "", ""
            if "PLACE" in tmp_data:
                place_str = ",".join(tmp_data["PLACE"])
            if "ORGANIZATION" in tmp_data:
                org_str = ",".join(tmp_data["ORGANIZATION"])
            if "ACCOUNT" in tmp_data:
                account_str = ",".join(tmp_data["ACCOUNT"])

            out += f'{value["label"]:<30}{value["role"]:<50}{place_str:<30}{org_str:<50}{account_str:<30}{value["skills"]}\n'
            if value["notes"]:
                out += f'\tNOTES: {value["notes"]}\n'
        return out

    def afterEditing(self):
        curr_graph = self.parentApp.getForm("MAIN").connection_graph
        matching_persons, neighbor_nodes = curr_graph.search_for_person_with_skill(
            self.query.value
        )
        additional_data = {}
        # for each person node with matching skills
        for person in neighbor_nodes:
            additional_data[person] = {}
            # for each neighbor node of the person node
            for neighbor_id in neighbor_nodes[person]:
                edge_info = neighbor_nodes[person][neighbor_id]
                if (
                    edge_info["kind"] == "BASEDIN"
                    and curr_graph.nodes[neighbor_id]["kind"] == "PLACE"
                ):
                    if "PLACE" not in additional_data[person]:
                        additional_data[person]["PLACE"] = []
                    additional_data[person]["PLACE"].append(
                        curr_graph.nodes[neighbor_id]["label"]
                    )
                elif (
                    edge_info["kind"] == "ASSOCWITH"
                    and curr_graph.nodes[neighbor_id]["kind"] == "ORGANIZATION"
                ):
                    if "ORGANIZATION" not in additional_data[person]:
                        additional_data[person]["ORGANIZATION"] = []
                    additional_data[person]["ORGANIZATION"].append(
                        curr_graph.nodes[neighbor_id]["label"]
                    )
                elif (
                    edge_info["kind"] == "ONACCOUNT"
                    and curr_graph.nodes[neighbor_id]["kind"] == "ACCOUNT"
                ):
                    if "ACCOUNT" not in additional_data[person]:
                        additional_data[person]["ACCOUNT"] = []
                    additional_data[person]["ACCOUNT"].append(
                        curr_graph.nodes[neighbor_id]["label"]
                    )
        table = self._tabulate_results(matching_persons, additional_data)
        npyscreen.notify_confirm(f"{table}", title="Results", wide=True)
        self.parentApp.setNextForm("MAIN")


class ConsoleSocialGraphTool(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainMenu, name="Social Graph Tool - Main Menu ()")
        self.addForm("LOADGRAPH", LoadGraph, name="Social Graph Tool - Load Graph")
        self.addForm("SAVEGRAPH", SaveGraph, name="Social Graph Tool - Save Graph")
        self.addForm("NEWGRAPH", NewGraph, name="Social Graph Tool - New Graph")
        self.addForm("ADDPERSON", AddPerson, name="Social Graph Tool - Add Person")
        self.addForm(
            "ADDEDGECHOICE",
            AddEdgeChoice,
            name="Social Graph Tool - Choose Edge Type to Add",
        )
        self.addForm("ADDEDGE", AddEdge, name="Social Graph Tool - Add Edge")
        self.addForm(
            "ADDNODECHOICE",
            AddNodeChoice,
            name="Social Graph Tool - Choose Node Type to Add",
        )
        self.addForm("ADDNODE", AddNode, name="Social Graph Tool - Add Node")
        self.addForm(
            "SKILLSEARCH", SkillSearch, name="Social Graph Tool - Skill Search"
        )
        self.addForm(
            "OVERWRITE", OverwriteGraph, name="Social Graph Tool - Overwrite Graph?"
        )


if __name__ == "__main__":
    TestApp = ConsoleSocialGraphTool().run()
