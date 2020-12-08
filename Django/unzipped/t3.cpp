#include <iostream>
#include <queue>
#include <unordered_set>
#include <vector>
using namespace std;

int main() {

ios_base::sync_with_stdio(false);
cin.tie(NULL);

int n,m;  cin >> n >> m;  
int deleted = 0;

unordered_set<int> adj_ls[n];
queue<int> q;

for(int i=0; i<n; i++) if(adj_ls[i].size() <= 2) q.push(i);

while(!q.empty() && q.size()>1){
	int k = q.front(); q.pop();
	int s = adj_ls[k].size();
	if(s==1){
		int x1 = *(adj_ls[k].begin());
		adj_ls[x1].erase(k);
		adj_ls[k].clear();
		if(adj_ls[x1].size() ==2) q.push(x1);
		deleted++;
	}
	if(s==2){
		auto z1 = adj_ls[k].begin();
		int x1 = *(z1);z1++;
		int x2 = *(z1);
		adj_ls[k].clear();
		adj_ls[x1].erase(k);
		adj_ls[x2].erase(k);
		adj_ls[x1].insert(x2);
		adj_ls[x2].insert(x1);
		if(adj_ls[x1].size()==2) q.push(x1);
		if(adj_ls[x2].size()==2) q.push(x2);
		deleted++;
	}
}

if(deleted == n-1){
	cout << "yes"<< endl;
	cout << 123 << endl;
} 
else cout << "no" << endl;



}