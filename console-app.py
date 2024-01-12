import npyscreen


class MainMenu(npyscreen.Form):
    def beforeEditing(self):
        self.name = f"Social Graph Tool - Main Menu ({self.current_file})"

    def create(self):
        self.current_file = None
        self.myDepartment = self.add(
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
        if act_on_this == "New Graph":
            self.parent.parentApp.switchForm("NEWGRAPH")
        elif act_on_this == "Load Graph":
            self.parent.parentApp.switchForm("LOADGRAPH")
        elif act_on_this == "Add Person":
            self.parent.parentApp.switchForm("ADDPERSON")
        elif act_on_this == "Add Node":
            self.parent.parentApp.switchForm("ADDNODE")
        elif act_on_this == "Add Edge":
            self.parent.parentApp.switchForm("ADDEDGE")
        elif act_on_this == "Search":
            self.parent.parentApp.switchForm("SEARCH")
        elif act_on_this == "Save Graph":
            self.parent.parentApp.switchForm("SAVEGRAPH")
        elif act_on_this == "Exit":
            self.parent.parentApp.switchForm(None)

    def actionHighlighted(self, act_on_this, key_press):
        self._select_next_form(act_on_this, key_press)


class LoadGraph(npyscreen.Form):
    def afterEditing(self):
        # TODO: load the graphml file here

        self.parentApp.getForm("MAIN").current_file = self.input_graph_file.value
        self.parentApp.setNextForm("MAIN")

    def create(self):
        self.input_graph_file = self.add(
            npyscreen.TitleText,
            name="Graph File Name:",
        )


class ConsoleSocialGraphTool(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainMenu, name="Social Graph Tool - Main Menu ()")
        self.addForm("LOADGRAPH", LoadGraph, name="Social Graph Tool - Load Graph")


if __name__ == "__main__":
    TestApp = ConsoleSocialGraphTool().run()
