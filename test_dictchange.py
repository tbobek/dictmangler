import unittest
from dictchange import DictMangler

class TestDictChange(unittest.TestCase): 
    def Test1(self): 
        mydict = {
            "a" : 2,
            "b" : "test", 
            "c" : {
                "date" : { "$date" : "2021-08-12" }, 
                "e": "current"
            },
            "f" : "some_value",
            "g" : [ { "date" : { "$date" : "2021-08-10"}}, {"foo" : "baz"}, {"bla": "blubb"}], 
            "h" : { "i" : { "date" : { "$date" : "2021-08-09" }}}
        }
        c = DictMangler()
        c.set_dict(mydict)
        result = c.nested_change("$date")
        expected = "2021-08-12"
        actual = result["g"]["date"]
        self.assertEqual(actual, expected, msg="1. got {}, expected {}".format(actual, expected))
        expected = "2021-08-10"
        actual = result["g"][0]["date"]
        self.assertEqual(actual, expected, msg="2. got {}, expected {}".format(actual, expected))
        expected = "2021-08-19"
        actual = result["h"]["i"]["date"]
        self.assertEqual(actual, expected, msg="3. got {}, expected {}".format(actual, expected))
        
        
if __name__ == "__main__": 
    unittest.main()