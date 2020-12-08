#include<bits/stdc++.h>

using namespace std;

long long int J(long long int n, int k){
	if (k==1) return n;
	if (n==1) return 1;
	if (n>=k) {
		long long int a = J(n-(n/k), k);
		long long int i;
		long long int j = a + (n/k)*k -(n+1);
		if(j>=0) i = (n/k)*k + a + j/(k-1);
		if(j<0) i = (n/k)*k + a;
		if(i>n) return i-n;
		else return i;
	}
	if (n<k) {
		long long int a = J(n-1, k);
		long long int i = (k%n)+a;
		if(i>n) return i-n;
		else return i;
	}
}

int main(){
	long long int n;
	int k;

	cin >> n >> k;

	cout<< J(n, k) << endl;
}