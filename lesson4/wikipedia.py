import sys
import collections
import time
import copy

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id) - 1
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src) - 1, int(dst) - 1)
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # return index of the title
    def find_index(self, title):
        for id in self.titles.keys():
            if(self.titles[id] == title):
                return id

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    # Return True if the shortst path was found. Return False if the shortest path was not found
    def find_shortest_path(self, start, goal, links, hw3):
        #------------------------#
        # Write your code here!  #
        if (start == goal):
            print(start)
            print(goal)
            return False
        
        start_index = self.find_index(start)
        goal_index = self.find_index(goal)

        queue = collections.deque()
        paths = {}
        
        queue.append(start_index)
        paths[start_index] = [start_index]

        while(len(queue) != 0):
            node = queue.popleft()
            
            for child_node in links[node]:
                if(paths.get(child_node) == None):
                    queue.append(child_node)
                    paths[child_node] = paths[node] + [child_node]

                    if(child_node == goal_index):
                        print("The path from", start, "to", goal, "is")
                        for node in paths[goal_index]:
                            print(self.titles[node])

                        # 宿題3のための操作
                        if hw3 == True:
                            for id in range (len(paths[goal_index]) - 1):
                                links[paths[goal_index][id]].remove(paths[goal_index][id+1])
                            
                        print()
                        return True
        
        print("no path from", start, "to", goal)
        return False
        #------------------------#
        pass

    # return True if the page ranks of all the nodes are not changed from the previous page ranks
    # |prev_page_ranks|, |page_ranks|: dictionaries of page ranks which you want to compare 
    def page_ranks_are_fixed(self, prev_page_ranks, page_ranks):
        for node_index in self.titles:
            if(abs(prev_page_ranks[node_index] - page_ranks[node_index]) > 0.1):
                return False
        return True

    # calculate the page ranks for one time
    def calculate_page_ranks(self, prev_page_ranks):
        page_ranks = {key: 0.15 for key in self.titles}
        distribute_all = 0

        for node_index in self.titles:
            if(len(self.links[node_index]) != 0):
                distribute_to_children = prev_page_ranks[node_index] * 0.85 / len(self.links[node_index])
                for child_node_index in self.links[node_index]:
                    page_ranks[child_node_index] += distribute_to_children
            else:
                distribute_all += prev_page_ranks[node_index] * 0.85
    
        for node_index in self.titles:
            page_ranks[node_index] += distribute_all / len(self.titles)

        return page_ranks

    # return the index of the node with the highest page rank in page_ranks
    def get_index_of_highest_ranks(self, page_ranks):
        most_popular_page_index = 0
        most_popular_page_ranks = 0
        for node_index in self.titles:
            if(most_popular_page_ranks < page_ranks[node_index]):
                most_popular_page_ranks = page_ranks[node_index]
                most_popular_page_index = node_index
        return most_popular_page_index

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        prev_page_ranks = {}
        page_ranks = {}
        prev_sum_of_page_ranks = 0
        sum_of_page_ranks = 0

        for node_index in self.titles:
            page_ranks[node_index] = 0
            prev_page_ranks[node_index] = 1
            prev_sum_of_page_ranks += 1

        while(self.page_ranks_are_fixed(prev_page_ranks, page_ranks) == False):
            page_ranks = self.calculate_page_ranks(prev_page_ranks)
            sum_of_page_ranks = sum(page_ranks.values())
            assert abs(sum_of_page_ranks - prev_sum_of_page_ranks) < 0.01
            prev_page_ranks = page_ranks
            prev_sum_of_page_ranks = sum_of_page_ranks            
        
        print("The most popular page is:")
        most_popular_index = self.get_index_of_highest_ranks(page_ranks)
        print(self.titles[most_popular_index])
        #------------------------#
        pass

    # Do something more interesting!!
    # Find more short paths. The function finds the shortest path, then it will find another path which doesn't use the path earlier.
    # The function continues to find the shortest path until it doesn't find any path  
    def find_more_short_paths(self, start, goal):
        #------------------------#
        # Write your code here!  #
        links = copy.deepcopy(self.links)

        shortest_path_exists = True
        count = 0
        while(shortest_path_exists):
            shortest_path_exists = self.find_shortest_path(start, goal, links, True)
            count += 1
        print("The number of paths is", count - 1)
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則", wikipedia.links, False)
    # wikipedia.find_most_popular_pages()
    wikipedia.find_more_short_paths("渋谷", "パレートの法則")
