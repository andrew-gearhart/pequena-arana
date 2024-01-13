import npyscreen
from social_graph_tool.connection_graph import (
    ConnectionGraph,
    import_graph_from_graphml_file,
    export_graph_to_graphml_file,
)


# TODO: ADDEDGE, ADDNODE, SEARCH
# ADDEDGE will need to have a selector for the edge types: ASOCWITH, ONACCOUNT, BASEDIN
# ADDNODE will need to have a selector for the node types: PERSON, PLACE, ORG, ACCOUNT
# SEARCH will likely have a modified attribute search inside of connection_graph (beforeEditing), and then display the results in a list.
class MainMenu(npyscreen.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph_name = None
        self.connection_graph = None

    def beforeEditing(self):
        self.name = f"Social Graph Tool - Main Menu ({self.graph_name})"

    def create(self):
        self.menu_value = self.add(
            MainMenuSelector,
            scroll_exit=True,
            max_height=8,
            name="Main Menu Options",
            values=[
                "New Graph",
                "Load Graph",
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
            self.handle_destructive_action("NEWGRAPH")
        elif act_on_this == "Load Graph":  # Destructive
            self.handle_destructive_action("LOADGRAPH")
        elif act_on_this == "Add Person":
            self.parent.parentApp.switchForm("ADDPERSON")
        elif act_on_this == "Add Node":
            npyscreen.notify_confirm("Function not implemented!", title="Error")
            self.parent.parentApp.switchForm("MAIN")
        elif act_on_this == "Add Edge":
            npyscreen.notify_confirm("Function not implemented!", title="Error")
            self.parent.parentApp.switchForm("MAIN")
        elif act_on_this == "Search":
            npyscreen.notify_confirm("Function not implemented!", title="Error")
            self.parent.parentApp.switchForm("MAIN")
        elif act_on_this == "Save Graph":
            self.parent.parentApp.getForm("SAVEGRAPH").next_form = "MAIN"
            self.parent.parentApp.switchForm("SAVEGRAPH")
        elif act_on_this == "Exit":  # Destructive
            self.handle_destructive_action(None)

    # Note: Currently overwriting any existing graph without warning.
    def handle_destructive_action(self, next_form):
        self.parent.parentApp.switchForm(next_form)

    def actionHighlighted(self, act_on_this, key_press):
        self._select_next_form(act_on_this, key_press)


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
        self.parentApp.setNextForm("MAIN")

    def create(self):
        self.graph_name = self.add(
            npyscreen.TitleText,
            name="New Graph Name:",
        )


# Note: Currently overwriting any existing graph file without warning.
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
            npyscreen.TitleText,
            name="Save File Name:",
        )

    def afterEditing(self):
        export_graph_to_graphml_file(
            self.parentApp.getForm("MAIN").connection_graph, self.save_file.value
        )
        self.parentApp.setNextForm(self.next_form)


class AddPerson(npyscreen.Form):
    def beforeEditing(self):
        curr_graph = self.parentApp.getForm("MAIN").connection_graph
        if not curr_graph:
            npyscreen.notify_confirm("No open graph to add person to!", title="Error")
            self.parentApp.setNextForm("MAIN")

    def create(self):
        self.person_name = self.add(
            npyscreen.TitleText,
            name="Person Name:",
        )
        self.person_place = self.add(
            npyscreen.TitleText,
            name="Person Place:",
        )
        self.person_org = self.add(
            npyscreen.TitleText,
            name="Person Org:",
        )
        self.person_account = self.add(
            npyscreen.TitleText,
            name="Person Account:",
        )
        self.person_skills = self.add(
            npyscreen.TitleText,
            name="Person Skills (CSV string):",
        )

    def afterEditing(self):
        curr_graph = self.parentApp.getForm("MAIN").connection_graph
        curr_graph.add_person(
            self.person_name.value,
            place=self.person_place.value,
            org=self.person_org.value,
            account=self.person_account.value,
            skills=self.person_skills.value,
        )
        self.parentApp.setNextForm("MAIN")


class ConsoleSocialGraphTool(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainMenu, name="Social Graph Tool - Main Menu ()")
        self.addForm("LOADGRAPH", LoadGraph, name="Social Graph Tool - Load Graph")
        self.addForm("SAVEGRAPH", SaveGraph, name="Social Graph Tool - Save Graph")
        self.addForm("NEWGRAPH", NewGraph, name="Social Graph Tool - New Graph")
        self.addForm("ADDPERSON", AddPerson, name="Social Graph Tool - Add Person")


if __name__ == "__main__":
    TestApp = ConsoleSocialGraphTool().run()
