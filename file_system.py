''' requirement:
A file system with directory and file.
Should be able to search file according to different criteria.
Criteria can be a AND/OR combination of name matching/size etc.
'''

from abc import ABC, abstractmethod

# File interface and implementations:
class Node(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def isDir(self):
        pass
    
    def __str__(self):
        return self.name
    
class File(Node):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size
        
    def isDir(self):
        return False
    
class Directory(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = []
    
    def isDir(self):
        return True

# Filter interface and implementations:
class Criteria(ABC):
    def __init__(self):
        self.criteria = []
    
    @abstractmethod
    def judge(self, file):
        pass

class CriteriaAnd(Criteria):
    def __init__(self, criteria):
        self.criteria = criteria
        
    def judge(self, file):
        for criterion in self.criteria:
            if criterion.judge(file):
                continue
            else:
                return False
        return True
        
class CriteriaOr(Criteria):
    def __init__(self, criteria):
        self.criteria = criteria
        
    def judge(self, file):
        for criterion in self.criteria:
            if criterion.judge(file):
                return True
        return False

class NameCriterion(Criteria):
    def __init__(self, keyword):
        self.keyWord = keyword
    def judge(self, file):
        if self.keyWord in file.name:
            return True
        return False

class SizeBiggerCriterion(Criteria):
    def __init__(self, size):
        self.size = size
    def judge(self, file):
        if file.size > self.size:
            return True
        return False

# System implementation
class System(object):
    def __init__(self, root):
        self.root = root
        
    def searchForFiles(self, criteria):
        res = []
        self.dfs(res, criteria, self.root)
        return res
    
    def dfs(self, res, criteria, node):
        if not node.isDir():
            if criteria.judge(node):
                res.append(node)
            return
        if node.isDir():
            for child in node.children:
                self.dfs(res, criteria, child)


# Test case
dir_l0 = Directory('dir_l0')
file_l0_f1 = File('file_l0_f1.txt', 5)

dir_l1_d1 = Directory('dir_l1_d1')
file_l1_f1 = File('file_l1_f1.txt', 3)

dir_l0.children = [file_l0_f1, dir_l1_d1]
dir_l1_d1.children = [file_l1_f1]

print('Test_and:')
system = System(dir_l0)
criteria = CriteriaAnd([NameCriterion('txt'), SizeBiggerCriterion(4)])
for file in system.searchForFiles(criteria):
    print(file)

print('Test_or:')
criteria = CriteriaOr([NameCriterion('txt'), SizeBiggerCriterion(4)])
for file in system.searchForFiles(criteria):
    print(file)
