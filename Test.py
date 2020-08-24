
import win32com.client




def test():
    src_path = "C:\\Users\\sanam\Desktop\\AttomusFiles\\"
    print("Hello")
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    msg = outlook.OpenSharedItem(r"C:\Users\sanam\Desktop\AttomusFiles\Test.msg")
    text = msg.Body


if __name__ == '__main__':
    test()
