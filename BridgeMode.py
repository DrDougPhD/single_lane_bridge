class BridgeMode():
  One_at_a_Time = 0
  One_direction = 1


  def __contains__(self, mode):
    # Convenience function to test if the user supplied a valid
    #  bridge mode upon initialization.
    #  ex. if (mode in Bridge_Mode): # do something
    #      else: # error
    if mode == 0 or mode == 1:
      return True
    return False

