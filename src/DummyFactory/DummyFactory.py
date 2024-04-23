from Entities.Team import Team
from Entities.Player import Player
from Game.Game import *
from Tournament.Tournament import *
import math


def generate_teams(start_teamid: int, start_playerid: int, num: int) -> list[Team]:
    result = []
    for i in range(1,num+1):
        print(i)
        player_1 = Player(
            id=start_playerid, 
            name=f"player_{start_playerid}",
            nickname=f"nickname_{start_playerid}",
            walk_on_music= "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        start_playerid += 1
        player_2 = Player(
            id=start_playerid, 
            name=f"player_{start_playerid}",
            nickname=f"nickname_{start_playerid}",
            walk_on_music= "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        result.append(Team(
            id=start_teamid,
            team_name=f"team_{start_teamid}",
            players=[player_1, player_2]
        ))
        start_teamid += 1
    return result

def generate_games(num_games: int, teams_per_game: int, teams: list[Team], start_gameid: int, gamemode: Game_Mode) -> list[Game]:
    result = []
    check_len = len(teams)/teams_per_game
    index_end = teams_per_game
    index_start = 0

    if check_len.is_integer() == False:
        raise ValueError(f"Number of teams must be even. Number of teams= {len(teams)}")
    
    for i in range(1,num_games+1):
        print(index_start, index_end)
        result.append(Game(
            game_id= start_gameid,
            group_name= f"group_{start_gameid}",
            teams= teams,
            game_mode= gamemode,
            sets={team.id: list() for team in teams[index_start:index_end]},
            current_set= Set(legs={team.id: list() for team in teams[index_start:index_end]}),
            current_leg= Leg(points={team.id: gamemode.points_per_leg for team in teams[index_start:index_end]}, rounds= {team.id: list() for team in teams[index_start:index_end]}),
            
        ))
        index_start = index_end
        index_end += teams_per_game
        
    return result

def generate_groupstage(teams: list[Team], num_groups: int, start_groupid: int) -> GroupStage:
    gamemode = Game_Mode(sets_to_win=3, legs_to_win_set=3, points_per_leg=501, check_out=Check_Out.DOUBLE_OUT, check_in=Check_In.STRAIGHT_IN)
    result = GroupStage(teams, [gamemode])
    index_end = len(teams)/num_groups
    index_start = 0
    

    if index_end < 1:
        raise ValueError(index_end)
    else:
        index_end = int(math.ceil(index_end))

    for i in range(1, num_groups+1):
        if index_end >= len(teams):
            index_end = -1
        result.create_group(
            start_id=start_groupid, 
            name=f"group_{start_groupid}",
            group_teams=teams[index_start:index_end],
            game_mode=gamemode,
            num_games_per_opponent=1,
            placement_to_advance=2)
        
        index_start = index_end
        index_end += index_end

        return result
