from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast("这是一个测试消息", "从前有只羊，它一直在山上吃草，后来有一天它不见了", icon_path="f.ico", duration=-1)
