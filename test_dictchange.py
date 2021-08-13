import unittest
import json
from dictchange import DictMangler

class TestMain(unittest.TestCase): 
    def test_nested_change(self): 
        """basic test of reducing one key value pair to its value 
        """
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
        actual = result["c"]["date"]

        self.assertEqual(actual, expected, msg="1. got {}, expected {}".format(actual, expected))
        expected = "2021-08-10"
        actual = result["g"][0]["date"]
        self.assertEqual(actual, expected, msg="2. got {}, expected {}".format(actual, expected))
        expected = "2021-08-09"
        actual = result["h"]["i"]["date"]
        self.assertEqual(actual, expected, msg="3. got {}, expected {}".format(actual, expected))
        
    def test_dict2list1(self):
        """handling of array should produce proper output
        """
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
        result = DictMangler.dict2list(mydict)
        actual = result[0]
        expected = "a; 2"
        self.assertEqual(actual, expected, msg="got {}, expected {}".format(actual, expected))

        
    def test_dict2list2(self):
        """input document now has array with dicts, two entries in this array have 
        equal keys ("foo"). By enumeration with the array indices, the final output keys
        should be unique (tested with key "g_1_foo")
        """
        mydict = {
            "a" : 2,
            "b" : "test", 
            "c" : {
                "date" : { "$date" : "2021-08-12" }, 
                "e": "current"
            },
            "f" : "some_value",
            "g" : [ { "date" : { "$date" : "2021-08-10"}}, {"foo" : "baz"}, {"foo": "blubb"}], 
            "h" : { "i" : { "date" : { "$date" : "2021-08-09" }}}
        }
        result = DictMangler.dict2list(mydict)
        actual = result[6]
        expected = "g_1_foo; baz"
        self.assertEqual(actual, expected, msg="got {}, expected {}".format(actual, expected))

    def test_load1(self):
        """a more real world scenario with loading data from a json file
        """
        mydict = {}
        with open("test.json") as f: 
            input_data = json.load(f)
        if isinstance(input_data, list): 
            mydict["data"] = input_data
        else: 
            mydict = input_data
        result = DictMangler.dict2list(mydict)
        actual = result[0]
        expected = "data_0_type; -"
        self.assertEqual(actual, expected, msg="got {}, expected {}".format(actual, expected))


if __name__ == "__main__": 
    unittest.main()