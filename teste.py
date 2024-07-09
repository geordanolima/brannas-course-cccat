
class BasePresenter():
    def exception_handler(self, method, params):
        try:
            result = method(*params)
            return result.dict()
        except Exception as error:
            print(error)


def test_method(p1, p2, p3):
    print(f"p1={p1} | p2={p2} | p3={p3}")
    x = {}
    x["p1"] = p1
    x["p2"] = p2
    x["p3"] = p3
    return x


z = ["9 d", 2, "p3"]
BasePresenter().exception_handler(method=test_method, params=z)
