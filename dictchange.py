import sys
import json



class DictMangler: 
    def __init__(self): 
        self.data = {}
        self.mdata = {}
        self.path = []

    def set_dict(self, d): 
        self.data = d

    def nested_change(self, k : str): 
        """ removes a key k and replaces its value to be the value of the key of the upper level
        e.g. if input data is { "a" : { "date" : { "$date" : "2021-08-12" }}} 
        and key is "$date" the output will be 
        { "a" : { "date" : "2021-08-12" }} 

        Motivation for this function is because Mongodb queries return such nested date and 
        timestamp formats that can be simplified 
        
        Args:
            k (str): key 

        Returns:
            dict : the modified dictionary
        """
        self.path = []
        self.mdata = self.data
        self.nested_change_rec(k, self.data)
        return self.mdata

    def __nested_set(self, dic, keys, value):
        for key in keys[:-1]:
            #dic = dic.setdefault(key, {})
            dic = dic[key]
        dic[keys[-1]] = value

    def nested_change_rec(self, k, d): 
        for key, value in d.items():
            if key == k: 
                if len(self.path)>0: 
                    self.__nested_set(self.mdata, self.path, value)
            elif isinstance(value, dict): 
                self.path.append(key)
                self.nested_change_rec(k, value)
            elif isinstance(value, list):
                self.path.append(key)
                for i, v in enumerate(value): 
                    self.path.append(i)
                    self.nested_change_rec(k, v)
                self.path.pop()

        if len(self.path)>0: 
            self.path.pop()

 

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

def main():
    print("start")
    print("test1")
    c = DictMangler()
    c.set_dict(mydict)
   
    newdic = c.nested_change("$date")
    print(newdic)

    print("end")

if __name__ == "__main__": 
    main()
