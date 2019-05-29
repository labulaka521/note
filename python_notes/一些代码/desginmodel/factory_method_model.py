from abc import ABCMeta, abstractclassmethod

# 定义一个Section抽象类来定义一个区是关于哪方面内容的
# 再提供一个抽象方法descripe
class Section(metaclass=ABCMeta):
    @abstractclassmethod
    def describe(self):
        pass

class PersonalSection(Section):
    def describe(self):
        pass

class AlbumSection(Section):
    def describe(self):
        print("Album Section")

class PatentSection(Section):
    def describe(self):
        print("patent Section")

class PublicationSection(Section):
    def describe(self):
        print("Publication Section")


# 创建名为Profile的抽象类Creator,提供了一个工厂方法
# createProfile(),
class Profile(metaclass=ABCMeta):
    def __init__(self):
        self.sections = []
        self.createProfile()
    
    @abstractclassmethod
    def createProfile(self):
        pass

    def getSections(self):
        return self.sections

    def addSection(self, section):
        self.sections.append(section)
    
# 创建两个ConcreteCreator类，即linkedin和facebook

class linkedin(Profile):
    def createProfile(self):
        self.addSection(PersonalSection())
        self.addSection(PatentSection())
        self.addSection(PublicationSection())

class facebook(Profile):
    def createProfile(self):
        self.addsection(PersonalSection())
        self.addSection(AlbumSection())

# 编写决定实例化哪个Creator类的客户端代码
if __name__ == '__main__':
    profile_type = input('Wich Profile you would like to create [Linkedin or Facebook]')
    profile = eval(profile_type.lower())()
    print("Creating Profile..", type(profile).__name__)
    print("Profile has sections --", profile.getSections())

