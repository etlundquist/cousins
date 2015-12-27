class Family(object):
    def __init__(self, founder):
        """ 
        Initialize with string of name of oldest ancestor
        """

        self.names_to_nodes = {}
        self.root = Member(founder)    
        self.names_to_nodes[founder] = self.root   

    def set_children(self, mother, list_of_children):
        """
        Set all children of the mother. 
        """
        # convert name to Member node (should check for validity)
        mom_node = self.names_to_nodes[mother]   
        # add each child
        for c in list_of_children:           
            # create Member node for a child   
            c_member = Member(c)               
            # remember its name to node mapping
            self.names_to_nodes[c] = c_member    
            # set child's parent
            c_member.add_parent(mom_node)        
            # set the parent's child
            mom_node.add_child(c_member)         
    
    def is_parent(self, mother, kid):
        """
        Returns True or False whether mother is parent of kid. 
        """
        mom_node = self.names_to_nodes[mother]
        child_node = self.names_to_nodes[kid]
        return child_node.is_parent(mom_node)   

    def is_child(self, kid, mother):
        """
        Returns True or False whether kid is child of mother. 
        """        
        mom_node = self.names_to_nodes[mother]   
        child_node = self.names_to_nodes[kid]
        return mom_node.is_child(child_node)

    def cousin(self, a, b):
        """
        Returns a tuple of (the cousin type, degree removed) 

        cousin type:
          -1 if a and b are the same node.
          -1 if either one is a direct descendant of the other
          >=0 otherwise, it calculates the distance from 
          each node to the common ancestor.  Then cousin type is 
          set to the smaller of the two distances, as described 
          in the exercises above

        degrees removed:
          >= 0
          The absolute value of the difference between the 
          distance from each node to their common ancestor.
        """
        
        # get the node values for the string parameters passed, and initialize the 'parent' nodes for the loop
        
        a_node = self.names_to_nodes[a] 
        b_node = self.names_to_nodes[b]
        a_par  = a_node
        b_par  = b_node
        
        # start the main loop, which checks to see whether either of the (a,b) nodes is a descendent of the current
        # (a,b) parent [a is by definition a descendent of of the current a parent, same for b]
        # the loop stops when you find an ancestor of either starting node s.t. both starting nodes are descendents
        # and what you want upon termination is the generational distance between each starting node and the common ancestor
        # this will allow you to determine cousin relation (min(dA,dB)) and removed relation (max(dA,Db) - cousin(a,b))
        
        while True:
            
            if (self.is_desc(a_par, b_node)[0]):
                a_dist = self.is_desc(a_par, a_node)[1]
                b_dist = self.is_desc(a_par, b_node)[1]
                break
            elif (self.is_desc(b_par, a_node)[0]):
                a_dist = self.is_desc(b_par, a_node)[1]
                b_dist = self.is_desc(b_par, b_node)[1]
                break
            else:
                a_par = a_par.get_parent() # if both start nodes are not descendents of either the current a or b 
                b_par = b_par.get_parent() # parent, then try the parents of those parents, etc.
        
        if   (a_dist == 0) and (b_dist == 0):
            return (-1, 0) # if both distances are zero, that means the nodes are the same person (I'm my own grandpa!)
        elif (a_dist == 0) or  (b_dist == 0):
            return (-1, abs(a_dist - b_dist)) # if one distance is zero, then the other node is a direct descendant
        else: # otherwise, the two nodes are cousins with the min distance-1 being the cousin relationship
            return (min(a_dist,b_dist)-1, max(a_dist,b_dist) - min(a_dist,b_dist))    
             
    def is_desc(self, s_node, f_node):
        '''function to search recursively through the tree from a given node to attempt to find another downstream node
        it will return (True, Dist) if the downstream node is a descendent, where Dist will be the number of parent links
        or generations in this case that separate the start node from the find node. these numbers are important because
        they will define the cousin/removed relationship based on the Dist of each cousin node to the first common ancestor'''
        
        queue  = [s_node] # set up a queue in which to search for the f_node, initially just the s_node
        levels = 0        # keep track of the number of generations between the start node and the find node
                      
        while len(queue) > 0:
            curqueue = queue[:]                  # copy the current queue to process this generation
            for node in curqueue:                # loop through this generation of children to search for the needle
                if (node is f_node):             # if the needle is found, return True and the generation distance
                    return (True, levels)
                else:
                    for child in node.children:  # if the node being checked doesn't make, append its children then remove it
                        queue.append(child)      # such that all its children go to the back of the line to search in the next
                queue.remove(node)               # iteration of the main While loop, but all of this generation is removed first
            levels += 1                          # increment the generation counter each time you search a full generation
        return (False, -1)
        