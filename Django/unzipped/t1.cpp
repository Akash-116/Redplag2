#include <iostream>
#include <queue>
#include <vector>
#include <list>
#include <unordered_set>
// #include <utility>
// #include <limits>
// #include <functional>
using namespace std;

queue<int> Q;


vector<unordered_set<int>> adjacent;

// vector<int> mdegree;

// vector<int> sdegree;



// struct HashFunc{
// 	int operator() (pair<int, int>const &P) const{
// 		int base = 1048577;  //prime factorisation is 17 * 61681.
// 		if(P.first > P.second)
// 			return ((long long int)P.second * (long long int)base + P.first) % 1000000007;
// 		else
// 			return ((long long int)P.first * (long long int)base + P.second) % 1000000007;
// 	}

// };



// struct Equiv{
// 	bool operator() (pair<int,int> const &P1, pair<int, int>const &P2 ) const{
// 		if(P1.first == P2.first && P1.second == P2.second) return true;
// 		else if(P1.first == P2.second && P1.second == P2.first) return true;
// 		else return false;
// 	}

// };


// unordered_set < pair<int, int>, HashFunc, Equiv> edges;








int main() {

	ios_base::sync_with_stdio(false);
	cin.tie(NULL);


	int n; cin >> n;  // vertices are 0,1,2,3,....n-1
	int m; cin >> m; //num of edges

	// mdegree.resize(n);
	adjacent.resize(n);
	// sdegree.resize(n);
	int existing = n;

	for(int iq=0; iq<m; iq++ ){

		int first; cin >> first;
		int second; cin >> second;
		// mdegree[first]++; mdegree[second]++;
		// pair <int, int> spam(first, second);

		// if(adjacent[first].find(second) == adjacent[first].end()){
			adjacent[first].insert(second);
			adjacent[second].insert(first);
			// sdegree[first]++; 
			// sdegree[second]++;
			// edges.insert(spam);
		// }

	}

	// can i ignore mdegree????

	for(int i=0; i<n; i++){
		if(adjacent[i].size() <= 2) Q.push(i);
	}


	while(!Q.empty() && Q.size()>1){

		int x = Q.front(); Q.pop();

		if(adjacent[x].size()==1){

			existing--;
			int adj = *(adjacent[x].begin());
			adjacent[x].clear();
			adjacent[adj].erase(x);
			// sdegree[x]=0;
			// sdegree[adj]--;
			if(adjacent[adj].size() ==2) Q.push(adj);
			//should i also remove edge from edges????

		}

		else if(adjacent[x].size()==2){

			existing--;
			auto p = adjacent[x].begin();
			int adjl = *(p);
			p++;
			int adjr = *(p);

			adjacent[x].clear();
			adjacent[adjl].erase(x);
			adjacent[adjr].erase(x);

			// sdegree[x]=0;
			// sdegree[adjr]--; sdegree[adjl]--;

			// pair <int, int> spam(adjl, adjr);

			// if(adjacent[adjl].find(adjr) == adjacent[adjl].end()){
				adjacent[adjl].insert(adjr);
				adjacent[adjr].insert(adjl);
				// sdegree[adjl]++; sdegree[adjr]++;
				// edges.insert(spam);
			// }

			if(adjacent[adjl].size()==2) Q.push(adjl);
			if(adjacent[adjr].size()==2) Q.push(adjr);
		}

	}

	if(existing == 1) cout << "yes"<< endl;
	else cout << "no"<< endl;

	// cout << numeric_limits<int>::max()<<endl;

}