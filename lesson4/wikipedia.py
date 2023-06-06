import sys
import collections

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


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        if (start == goal):
            # print(start)
            return

        queue = collections.deque()
        # paths = [""] * (len(self.titles))
        paths = {}
        # print(len(self.titles))

        for id in self.titles.keys():
            if(self.titles[id] == start):
                start_index = id
                break

        for id in self.titles.keys():
            if(self.titles[id] == goal):
                goal_index = id
                break

        queue.append(start_index)
        paths[start_index] = str(start_index)

        while(len(queue) != 0):
            node = queue.popleft()
            
            for child_node in self.links[node]:
                if(paths.get(child_node) == None):
                    # print(child_node)
                    queue.append(child_node)
                    paths[child_node] = paths[node] + "," + str(child_node)

                    if(child_node == goal_index):
                        print("The shortest pass from", start, "to", goal, "is")
                        # print("path is", paths[child_node])
                        ans_path = paths[child_node].split(",")
                        for i in range (len(ans_path)):
                            print(self.titles[int(ans_path[i])])
                        print()
        #------------------------#
        pass

    # return True if the page ranks are not changed from the previous page ranks
    def page_ranks_are_fixed(self, prev_page_ranks, page_ranks):
        for node_index in range (len(page_ranks)):
            if(abs(prev_page_ranks[node_index] - page_ranks[node_index]) > 0.1):
                return False
        return True

    def calculate_page_ranks(self, prev_page_ranks):
        page_ranks = [0.15] * len(self.titles)
        distribute_all = 0
        for node_index in self.titles:
            if(len(self.links[node_index]) != 0):
                distribute = prev_page_ranks[node_index] * 0.85 / len(self.links[node_index])
                for child_node_index in self.links[node_index]:
                    page_ranks[child_node_index] += distribute
            else:
                distribute_all += prev_page_ranks
        
        for node_index in range (len(self.titles)):
            page_ranks[node_index] += distribute_all / len(self.titles)

        return page_ranks



    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        prev_page_ranks = [0] * len(self.titles) 
        page_ranks = [1] * len(self.titles) 
        while(self.page_ranks_are_fixed(prev_page_ranks, page_ranks) == False):
            prev_page_ranks = page_ranks
            page_ranks = self.calculate_page_ranks(prev_page_ranks)

        most_popular_page_index = 0
        most_popular_page_ranks = 0
        for node_index in range (len(page_ranks)):
            if(most_popular_page_ranks < page_ranks[node_index]):
                most_popular_page_ranks = page_ranks[node_index]
                most_popular_page_index = node_index
        
        print("The most popular page is:")
        print(self.titles[most_popular_page_index])
        #------------------------#
        pass


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
