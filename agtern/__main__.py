from agtern.gui import Application
from agtern.backend import start_server

if __name__ == '__main__':
    start_server()
    app = Application()
    try:
        app.mainloop()
    except KeyboardInterrupt: # Ctrl+C
        pass # Do nothing and hide Traceback