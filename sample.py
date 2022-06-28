#
# @brief json 문장 등록 gui
#
# Created registerView.py on Thu Jun 02 2022
#
# @author kim jeonghoon <kyg1084@gmail.com>
#
# @copyright (c) 2022 DPJ
#


from tkinter import *
from tkinter.ttk import *
from pynput.keyboard import Listener, Key, KeyCode
import json
import clipboard

def inputView():
    root = Tk()
    root.title("문장 조합기")
    root.geometry('300x300')
    
    # TODO : 각 위젯 배치 조절

    # btn eventListener
    def btnInputClick():
        index = OptionList.index(variable.get())
        print(js_array[index]["data"])
        js_array[index]["data"].append(txt.get())
        print(js_array[index]["data"])
        with open('data/sentence_output.json', "w") as f:
            json.dump(js_array, f, indent=4)
    # ~btn eventListener

    # data load
    with open('data/sentence.json', "r") as f:
        js_array = json.load(f)
        OptionList = []
        for js in js_array:
            OptionList.append(js["name"])
        variable = StringVar(root)
        variable.set(OptionList[0])
    # data load

    # Gui paint
    def currTransparent(self):
        value = "투명값: " + str(scale.get())
        root.attributes('-alpha', scale.get())
        # root.attributes('-alpha', 0.5)
        # root.wm_attributes('-transparentcolor', root['bg'])

    scale = Scale(root, command=currTransparent, orient="horizontal", from_=0, to=1, value=1)
    scale.pack(side=TOP, anchor=NE)
    
    lbl = Label(root, text="문장 등록")
    lbl.pack()
    def setTextInput(text):
        textEntry.set(text)
    textEntry = StringVar()
    txt = Entry(root, textvariable = textEntry)
    txt.pack()
    opt = OptionMenu(root, variable, *OptionList)
    opt.pack()
    btn = Button(root, text="등록", command=btnInputClick)
    btn.pack()
    lbl1 = Label(root, text=js_array)
    lbl1.pack()
    # ~Gui paint

    # with open('data/sentence.json') as f
    # json input  json_string = json.dump(json_obj, f, indent=2)

    # select box eventListener
    def callback(*args):
        print("selected {}".format(variable.get()))
        print("and index {}".format(OptionList.index(variable.get())))
        lbl1.configure(text="{}".format( js_array[OptionList.index(variable.get())]["data"] ))
    # ~select box eventListener

    variable.trace("w", callback)


    store = set()

    HOT_KEYS = {
        # TODO combination & paste clipboard  # press-side
        'autoCopy': set([ Key.ctrl_l, KeyCode(char= chr(ord("C")-64))])
    }


    def autoCopy():
        print( 'auto copy () - {}'.format(clipboard.paste()))
        setTextInput(clipboard.paste)
        # txt.delete(0, "end")
        # txt.insert(0, clipboard.paste())

    def handlePress( key ):
        store.add( key )
        print( 'Press: {}'.format( store ))

    def handleRelease( key ):
        print( 'Released: {}'.format( key ))
        # INPUT HOT KEY FUNCTION
        for action, trigger in HOT_KEYS.items():
            CHECK = all([ True if triggerKey in store else False for triggerKey in trigger ])
            if CHECK:
                try:
                    func = eval( action )
                    if callable( func ):
                        func()
                except NameError as err:
                    print( err )

        if key in store:
            store.remove( key )
        if key == Key.esc:
            root.destroy()
            quit(0)

    listener =  Listener(on_press=handlePress, on_release=handleRelease)
    listener.start()
    root.mainloop()
inputView()