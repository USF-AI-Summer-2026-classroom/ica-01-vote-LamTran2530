from candidate import Candidate
from voter import Voter

import random
import heapq


class VotingSystem:
    def __init__(self):
        self.candidates = []
        self.voters = []

    def generate_candidates(self, count):
        names = ['Aang', 'Katara', 'Sokka', 'Zuko', 'Iroh', 'Appa', 'Momo', 'Toph', 'Azula', 'Suki', 'Ozai', 'Mai', 'Ty']
        self.candidates = [
            Candidate(
                name=names[i],
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]

    def generate_voters(self, count):
        self.voters = [
            Voter(
                id=i + 1,
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]

    def voter_ranked_choices(self):

        ballots = []

        for voter in self.voters:
            heap = [ (abs(voter.leaning - c.get_leaning()), c)

                for c in self.candidates
            ]
            heapq.heapify(heap)
            ballots.append(heap)

        return ballots

    def count_votes(self, ballots, eliminated):

        active = [c for c in self.candidates if c not in eliminated]

        tally = {c: 0 for c in active}

        for ballot in ballots:

            while ballot and ballot[0][1] in eliminated:
                heapq.heappop(ballot)

            if ballot:
                tally[ballot[0][1]] += 1

        return tally

    def election_results(self):

        eliminated = set()
        ballots = self.voter_ranked_choices()
        round_number = 1

        while True:

            tally = self.count_votes(ballots, eliminated)
            total_votes = sum(tally.values())

            print(f"\nRound {round_number}")
            for candidate, votes in sorted(tally.items(), key=lambda item: -item[1]):
                print(f"  {candidate.get_name()}: {votes} votes ({votes / total_votes * 100:.1f}%)")

            for candidate, votes in tally.items():
                if votes > total_votes / 2:
                    print(f"\n Winner: {candidate.get_name()} ({votes}/{total_votes} votes, {votes / total_votes * 100:.1f}%)")
                    return candidate

            min_votes = min(tally.values())

            if min_votes == max(tally.values()):
                names = ", ".join(c.get_name() for c in tally)
                print(f"\n Tie between: {names}")
                return list(tally.keys())[0]

            for c in [c for c, v in tally.items() if v == min_votes]:
                eliminated.add(c)
                print(f" Candidate eliminated: {c.get_name()} ")

            remaining = [c for c in self.candidates if c not in eliminated]
            if len(remaining) == 1:
                print(f"\n Winner: {remaining[0].get_name()}")
                return remaining[0]

            round_number += 1

if __name__ == "__main__":
    voting_system = VotingSystem()

    voting_system.generate_candidates(5)
    voting_system.generate_voters(100)

    print("Current election")
    voting_system.election_results()
