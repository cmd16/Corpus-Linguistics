import re
regex_list = ["((\w+_(PP\$|DT)(\s\w|_JJ)?(\s\w+_(NN|NNS))\s?){2}", "(\w+_(PP\$|DT)(\s\w+_(NN|NNS))(\s\w+_RB)?(\s\w+_JJ)(,_,)?",
              "(\w+_(PP\$|DT)?(\s\w+_JJ)?(\s\w+_(NN|NNS))(\s\w+_(JJ|RB))?(\s\w+_IN))", "(\w+_PP\$|DT))?(\s\w+_(JJ|RB))?"
                                                    "(\s\w+_(NN|NNS))(\s\w+_(JJ|RB))?(\s\w+_(VVG|VVN|VBN))(\s\w+_IN)?"]
