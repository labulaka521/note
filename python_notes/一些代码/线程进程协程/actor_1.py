from actor import Actor

class TaggedActor(Actor):
    def run(self):
        while True:
            tag, *payload = self.recv()
            getattr(self, 'do_'+tag)(*payload)

    def do_A(self,x):
        print('Running A: ',x)
        return 'Running A: {}'.format(x)

    def do_B(self,x,y): 
        print('Running B: ',x,y)

