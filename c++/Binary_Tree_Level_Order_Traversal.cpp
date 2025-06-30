/*

35 / 35 test cases passed.
Runtime: 0 ms
Memory Usage: 16.8 MB
somehow beats 100% of other submissions on Leetcode

nodes entered in as nested ints ie root = [3,9,20,null,null,15,7] supplied to mean 

  
   3
  /\
9    20
     /\
    15 7

code reads in root and returns a vector of vector of integers, where node points to the next two below it
Used some basic STL back inserter stuff for memory efficiency and breadth first entered all the nodes since that's the solution the root entry seemed to suggest
basic idea is running two deques of TreeNode object pointers with the current row and the last row to effectively link up the objects in order
code is pretty efficient but readability could be much better, possible that deque could be replaced with more memory efficient container with better planning

 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        
        vector<vector<int>> treeple;
        vector<int> holder;
        vector<int> values;
        vector<int> pairNodes;

        deque<TreeNode*> lastRow;
        deque<TreeNode*> nextRow;

        

        lastRow.push_back(root);

        if (root == nullptr) {
            
            return treeple;

        }

        do {

            for (auto &elem: lastRow) {  //runs for every node L>>R in the last row

                holder.push_back(elem -> val);  //fills holder with L>>R num vals
                nextRow.push_back(elem -> left); //fills next row with pointers L>>R
                nextRow.push_back(elem -> right);

            }


            for (reverse_iterator it = holder.rbegin(); it != holder.rend(); ++it) {

                values.push_back(*it);

            } //fills values in reverse

            while (!values.empty()) {

                pairNodes.push_back(values.back());
                values.pop_back();
                
                
                

            } //loads two leftmost values into pairnodes and pairnodes into treeple

            treeple.push_back(pairNodes);
            pairNodes.clear();

            //put nextrow into last row

            lastRow.clear();
            copy_if(nextRow.begin(), nextRow.end(), back_inserter(lastRow), [](TreeNode* nod) { return nod != nullptr; });

            nextRow.clear();    
            holder.clear();     

        } while (!lastRow.empty());

        return treeple;

    }
};
