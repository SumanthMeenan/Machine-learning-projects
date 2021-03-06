import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import pandas as pd

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment

        #super is used to inherit the attributes and methods of
        #Agent class. as soon as super runs the __init__ function of
        #Agent will run.

        self.planner = RoutePlanner(self.env, self)  # Create a route planner

        #here we are passing self.env as a env arg and self as a
        #self as a agent arg for RoutePlanner class

        self.valid_actions = self.env.valid_actions  # The set of valid actions

        #here we are setting the valid_actions attribute of Learning
        #agent to Environment's valid_action attribute ie
        #self.env.valid_actions and those are
        #valid_actions = [None, 'forward', 'left', 'right']


        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        self.t = 0 #time step
        random.seed(1177)

    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)

        #here we are using the same planner attribute of LearningAgent
        #defined earlier, which is a RoutePlanner object. So we can call
        #route_to() method on it, which only takes one agrument which
        #is, destination,if destination is not provided, any random
        #intersection is taken as destination

        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        if testing:
            self.epsilon = 0.0
            self.alpha = 0.0
        else:
            # self.epsilon = self.epsilon - 0.05 #epsilon decreases linearly with trails
            self.t += 1.0
            # self.epsilon = 1.0/(self.t**2)
            # self.epsilon = 1.0/(self.t**2 + self.alpha*self.t)
            # self.epsilon = 1.0/(self.t**2 - self.alpha*self.t)
            # self.epsilon = math.fabs(math.cos(self.alpha*self.t))
            # self.epsilon = math.fabs(math.cos(self.alpha*self.t))/(self.t**2)
            # self.epsilon = 1.0/(self.t**2)
            self.epsilon = math.fabs(math.cos(self.alpha*self.t))

        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent
        # When learning, check if the state is in the Q-table
        #   If it is not, create a dictionary in the Q-table for the current 'state'
        #   For each action, set the Q-value for the state-action pair to 0

        # helper to create state string
        def xstr(s):
            if s is None:
                return 'None'
            else:
                return str(s)
        
        state = xstr(waypoint) + "_" + inputs['light'] + "_" + xstr(inputs['left']) + "_" +  xstr(inputs['oncoming'])
        if self.learning:
            self.Q[state] = self.Q.get(state, {None:0.0, 'forward':0.0, 'left':0.0, 'right':0.0})
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state
        # preset an initialization value that should be replaced by a more valid Q value in the loop.
        maxQ = -1000.0
        for action in self.Q[state]:
            if maxQ < self.Q[state][action]:
                maxQ = self.Q[state][action]
        return maxQ


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        if self.learning:
            self.Q[state] = self.Q.get(state, {None:0.0, 'forward':0.0, 'left':0.0, 'right':0.0})

        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state

        if not self.learning:
            action = random.choice(self.valid_actions)
        else:
            if self.epsilon > 0.01 and self.epsilon > random.random():
                action = random.choice(self.valid_actions)
            else:
                valid_actions = []
                maxQ = self.get_maxQ(state)
                for act in self.Q[state]:
                    if maxQ == self.Q[state][act]:
                        valid_actions.append(act)
                action = random.choice(valid_actions)
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')

        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env,display = False,update_delay = 0)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run()


if __name__ == '__main__':
    run()
