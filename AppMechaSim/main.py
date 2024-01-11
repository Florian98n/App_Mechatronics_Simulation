import tkinter as tk
import Frames_File
import Buttons_Search_Addable_File
import Buttons_Addable_List_File
import Workspace_File
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def on_resize(event, my_frames, my_workspace):
    my_frames.on_resize(event)
    my_workspace.on_resize(event)


class Main(tk.Tk):

    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, *kwargs)
        self.root = self
        self.root.title("Path + name of file")
        self.root.geometry("800x250")
        self.root.minsize(400, 250)
        self.root.state("zoomed")

        self.my_frames = Frames_File.Frames(self.root)

        self.my_workspace = Workspace_File.Workspace(self.root,
                                                     self.my_frames.frame_workspace,
                                                     self.my_frames.button_list_canvas)
        self.my_addable_buttons = Buttons_Addable_List_File.Buttons(self.my_frames.button_list_canvas,
                                                                    self.my_workspace.add_object,
                                                                    self.my_workspace.delete_unplaced_object)
        self.my_workspace.add_functions_for_buttons(self.my_addable_buttons.release_button)
        self.my_search = Buttons_Search_Addable_File.SearchZone(self.my_frames.frame_search_addable,
                                                                self.root,
                                                                self.my_addable_buttons.search_text,
                                                                self.my_addable_buttons.restore_from_search)
        self.root.bind('<Configure>', lambda event: on_resize(event, self.my_frames, self.my_workspace))
        self.root.mainloop()


if __name__ == '__main__':
    app = Main()
    app.mainloop()
