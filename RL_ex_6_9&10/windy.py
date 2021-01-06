from gym_minigrid.minigrid import *
from gym_minigrid.register import register

'''
Gym environment for RL book ex 6.9 & 6.10
Add to gym_minigrid/envs to work

Incorporates King's moves, wind, and
negative step reward

To add environment to gym_minigrid:

git clone https://github.com/maximecb/gym-minigrid.git
cd gym-minigrid/gym_minigrid/envs

put windy.py in envs
add to __init__.py in envs:
    "from gym_minigrid.envs.windy import *"

pip3 install -e .

'''

DIR_TO_VEC = [    
    # N (negative Y)
    np.array((0, -1)),    
    # NE
    np.array((1, -1)),
    # E (positive X)
    np.array((1, 0)),    
    # SE
    np.array((1, 1)),
    # S (positive Y)
    np.array((0, 1)),
    # SW
    np.array((-1, 1)),
    # W (negative X)
    np.array((-1, 0)),
    # NW
    np.array((-1, -1))
]

class WindyEnv(MiniGridEnv):
    class Actions(IntEnum):
        # King's moves:
        N = 0
        NE = 1
        E = 2
        SE = 3
        S = 4
        SW = 5
        W = 6
        NW = 7
        stop = 8
        # Done completing task
        done = 9
    
    def __init__(
        self,
        width=10,
        height=7,
        agent_start_pos=(1, 3),
        agent_start_dir=0
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir
        
        super().__init__(
            width = width, 
            height = height, 
            max_steps = 4 * width * height, 
            see_through_walls = True
        )
        self.actions = WindyEnv.Actions
        self.action_space = spaces.Discrete(len(self.actions))
        self.reward_range = (-1, 1)
        self.wind = [0, 0, 0, 0, -1, -1, -1, -2, -2, -1, 0, 0]
    
    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal square
        self.put_obj(Goal(), self.width - 4, int(np.ceil(self.height / 2)) - 1)

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "get to the green goal square but its windy"
        
    @property
    def dir_vec(self):
        """
        Get the direction vector for the agent, pointing in the direction
        of forward movement.
        """
        assert self.agent_dir >= 0 and self.agent_dir < 8
        return DIR_TO_VEC[self.agent_dir]

    def blow_wind(self):
    	return np.array((0, self.wind[self.agent_pos[0]]))
    
    def move_forward(self, move=True):   
        # Get the position in front of the agent
        if move:
            fwd_pos = self.front_pos + self.blow_wind()
        else:
            fwd_pos = self.agent_pos + self.blow_wind()
        fwd_pos[0] = min(max(fwd_pos[0], 1), self.width - 2)
        fwd_pos[1] = min(max(fwd_pos[1], 1), self.height - 2)
        # Get the contents of the cell in front of the agent
        fwd_cell = self.grid.get(*fwd_pos)

        done = False

        if fwd_cell == None or fwd_cell.can_overlap():
            self.agent_pos = tuple(fwd_pos)
        if fwd_cell != None and fwd_cell.type == 'goal':
            done = True
        if fwd_cell != None and fwd_cell.type == 'lava':
            done = True
            
        return done

    def step(self, action):
        self.step_count += 1
        reward = -1
        done = False


        if self.actions(action) == self.actions.done:
            pass
        elif self.actions(action) in self.actions:
            self.agent_dir = action
            if self.actions(action) != self.actions.stop:
                done = self.move_forward()
            else:
                done = self.move_forward(False)
        else:
            assert False, "unknown action"

        if self.step_count >= self.max_steps:
            done = True

        obs = self.gen_obs()

        return obs, reward, done, {}
    
class WindyEnvDefault(WindyEnv):
    def __init__(self):
        super().__init__()
        
register(
    id = 'MiniGrid-Windy-10x7-v0',
    entry_point = 'gym_minigrid.envs:WindyEnvDefault'
)