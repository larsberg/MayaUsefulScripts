
if 'flattenArray' not in locals():

  def flattenArray(forest, maxSubIndex = 3):
    return [leaf for tree in forest for index, leaf in enumerate(tree) if index < maxSubIndex]

