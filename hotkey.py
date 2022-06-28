from pynput.keyboard import Listener, Key, KeyCode
import clipboard
# import win32api # window system control library
# win32api.WinExec('notepad.exe') # 메모장 실행

store = set()

HOT_KEYS = {
    'functionname': set([ Key.alt_l, KeyCode(char='1')]),
    # TODO combination & paste clipboard  # press-side
    # TODO copy key - register # release-side
    'autoCopy': set([ Key.ctrl_l, KeyCode(char= chr(ord("C")-64))])
}
def functionname():
    print("기능")
def autoCopy():
    print("copy")

def handlePress( key ):
    store.add( key )
    print( 'Press: {}'.format( store ))
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

def handleRelease( key ):
    print( 'Released: {}'.format( key ))

    if key in store:
        store.remove( key )
    if key == Key.esc:
        return False
    
with Listener(on_press=handlePress, on_release=handleRelease) as listener:
    listener.join()