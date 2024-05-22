// SPDX-License-Identifier: GPL-2.0-or-later


contract MockHookTarget {
    /// @notice If given contract is a hook target, it is expected to return the bytes4 magic value that is the selector
    /// of this function
    /// @return The bytes4 magic value (0x87439e04) that is the selector of this function
    function isHookTarget() external pure returns (bytes4){
        return this.isHookTarget.selector;
    }
}