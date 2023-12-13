from numpy import sign

global offset_ascii 
offset_ascii = 65


class Node():

    def __init__(self, x : int, y : int, name: str = '-'):
        self.x = x
        self.y = y
        self.name = name
        self.neighbours = []

    def add_neighbour(self, node : 'Node'):
        self.neighbours.append(node)

    def remove_neighbour(self, node : 'Node'):
        self.neighbours.remove(node)

    def get_neighbours(self):
        return [node.name for node in self.neighbours]
    



class Graph():
    
    def __init__(self, width : int, height : int, origin_name: str = None, dest_name: str = None):
        self.width = width
        self.height = height
        self.nodes = []
        self.create_graph()
        if origin_name is not None:
            self.origin = self.get_node_by_name(origin_name)
        if origin_name is not None:
            self.dest = self.get_node_by_name(dest_name)
        self.path = []
        self.directions = []
        self.current_pos = None
        self.going_to = None
        self.current_direction = [1, 0]
        self.test_8 = False

    def set_trajectory(self):
        if self.origin is None or self.dest is None:
            print("Plase define origin and destination!")
            return 
        
        self.path = self.BFS(self.origin.name, self.dest.name)
        self.directions = self.get_directions(self.path)
        self.current_pos = self.origin
        self.going_to = self.path.pop(0)
    
    def update_trajectory(self, verbose=False):
        new_dir = self.directions.pop(0)
        new_pos = self.path.pop(0)
        
        if verbose:
            print("You are currently at: " + str(self.current_pos))
            print("You currently have the following direction: " + str(self.current_direction))
            print("You need to go to: " + str(self.going_to))
        
        return new_pos, new_dir
    
    def get_next_action(self):

        if self.test_8:
            return 5

        if len(self.path) == 0:
            #Stop, found target
            return 1
        
        new_loc, new_dir = self.update_trajectory()

        x_new, y_new = new_dir
        x_old, y_old = self.current_direction
        self.current_direction = new_dir
        self.current_pos = self.going_to
        self.going_to = new_loc

        if x_old == x_new and y_old == y_new:
            #Go straight
            return 5
        
        if x_new + x_old == 0 and y_new == y_old:
            #Turn 180
            return 4
        if y_new + y_old == 0 and x_old == x_new:
            #Turn 180
            return 4
        
        if y_new == 0:

            if sign(y_old) == sign(x_new):
                #turn left
                return 3
            else:
                #turn right
                return 2
        
        if x_new == 0:

            if sign(x_old) == sign(y_new):
                #turn right
                return 2
            else:
                #turn left
                return 3
    
    def translate_actions(self, action):

        if action == 1:
            print("Stop")
        if action == 2:
            print("Turn right")
        if action == 3:
            print("Turn left")
        if action == 4:
            print("Turn 180 degrees")
        if action == 5:
            print("Pass")
        else:
            print(str(action))

    def simulate_path(self):
        action = self.get_next_action()
        count = 0
        while action != 1:
            print("---------")
            print("current pos: " + str(self.current_pos.name))
            print("going to: " + str(self.going_to.name))
            print("current dir: " + str(self.current_direction))
            self.translate_actions(action)
            if count == 2:
                action = self.obstacle_found()
            else:
                action = self.get_next_action()

            count += 1
    
    def obstacle_found(self):
        self.origin = self.current_pos
        self.remove_edge(self.current_pos.name, self.going_to.name)
        self.print_graph()
        print(self.origin.name)
        print(self.dest.name)
        self.path = self.BFS(self.origin.name, self.dest.name)
        self.directions = self.get_directions(self.path)
        self.current_direction = [-self.current_direction[0], -self.current_direction[1]]

        self.going_to = self.path.pop(0)

        #Turn 180º
        return 4

            


    def create_graph(self):

        for i in range(self.height):
            for j in range(self.width):
                self.nodes.append(Node(j, i, chr(offset_ascii+i*self.width + j)))
        
        #Add neighbours

        for node in self.nodes:

            #Horizontal neighbours
            if node.x != 0:
                node.add_neighbour(self.nodes[node.y*self.width + node.x-1])
            if node.x != self.width-1:
                node.add_neighbour(self.nodes[node.y*self.width + node.x+1])
            
            #Vertical neighbours
            if node.y != 0:
                node.add_neighbour(self.nodes[(node.y-1)*self.width + node.x])
            if node.y != self.height-1:
                node.add_neighbour(self.nodes[(node.y+1)*self.width + node.x])
            

    
    def print_graph(self):

        for i in range(self.height):
            for j in range(self.width):

                if j != 0:
                    if self.nodes[i*self.width+j-1] in self.nodes[i*self.width+j].neighbours:
                        print(" - ", end="")
                    else:
                        print("   ", end="")
                current_node = self.nodes[i*self.width+j]
                print(current_node.name, end="")
            print("")

            if i == self.width-1: continue
            for j in range(self.width):
                if self.nodes[(i+1)*self.width+j] in self.nodes[i*self.width+j].neighbours:
                    print ("|   ", end="")
                else:
                    print ("    ", end="")

            print("")

    def get_node(self, x : int, y: int):

        return self.nodes[y*self.height + x]
    
    def get_node_by_name(self, name:str):

        pos = ord(name)-offset_ascii

        return self.nodes[pos]
    
    def remove_edge(self, node1_name: str, node2_name: str):
        node1 = self.get_node_by_name(node1_name)
        node2 = self.get_node_by_name(node2_name)
        node1.neighbours.remove(node2)
        node2.neighbours.remove(node1)

    
    def dummy_path(self, origin_name: str, dest_name: str):
        
        origin = self.get_node_by_name(origin_name)
        dest = self.get_node_by_name(dest_name)

        delta_x = dest.x - origin.x
        delta_y = dest.y - origin.y
        print(origin.y)
        print(dest.y)
        path = []

        for i in range(1, delta_x+1):
            next_x = origin.x + i*sign(delta_x)
            path.append(graph.get_node(next_x, origin.y))

        for i in range(1, delta_y+1):
            next_y = origin.y + i*sign(delta_y)
            path.append(graph.get_node(origin.x+delta_x, next_y))
        
        return [node.name for node in path]
    
    def BFS(self, origin_name: str, dest_name: str, names_only=False):

        origin = self.get_node_by_name(origin_name)
        dest = self.get_node_by_name(dest_name)
        visited = set()
        to_visit = []
        parent = {}
        current_node = origin
        end = False
        while len(visited) < len(self.nodes):
            if current_node == dest:
                        end = True
                        break
            visited.add(current_node)
            for neighbour in current_node.neighbours:
                if neighbour not in visited:
                    parent[neighbour] = current_node
                    to_visit.append(neighbour)
            
            current_node = to_visit.pop(0)

        if not end:
            print("No path available!")
        else:
            path = []
            while(current_node != origin):
                path.append(current_node)
                current_node = parent[current_node]
            path.append(origin)
            path.reverse()
            
            if names_only:
                path = [node.name for node in path]

            return path
    
    def get_directions(self, path):
        directions = []
        path_copy = path.copy()
        while True:
            current_node = path_copy.pop(0)
            direction = [0,0]
            if len(path_copy) == 0: return directions

            if path_copy[0].x < current_node.x:
                direction[0] = -1
            elif path_copy[0].x > current_node.x:
                direction[0] = 1
            
            if path_copy[0].y < current_node.y:
                direction[1] = -1
            elif path_copy[0].y > current_node.y:
                direction[1] = 1

            directions.append(direction)

   
if __name__ == "__main__":
    graph = Graph(5, 5, "A", "S")
    #graph.remove_edge("A", "B")
    graph.print_graph()
    #print(graph.get_node_by_name("Y").get_neighbours())
    #print(graph.dummy_path("A", "M"))
    #print(graph.get_node_by_name("B").x)
    #print(graph.get_node_by_name("B").y)
    #print(graph.BFS("A", "B", names_only=True))
    #path = graph.BFS("Q", "A")
    #print([node.name for node in path])
    graph.set_trajectory()
    graph.simulate_path()
    #way back
    final_dir = graph.current_direction
    graph = Graph(5, 5, "S", "A")
    graph.current_direction = final_dir
    graph.set_trajectory()
    graph.simulate_path()
    




    
