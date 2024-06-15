import "../Base/abstractBase.spec";


// used to test running time
use builtin rule sanity;

methods{
    function isRecognizedCollateralHarness(address collateral) external returns (bool) envfree;
    function getLTVConfigHarness(address collateral) external returns(Type.LTVConfig memory) envfree;
}


//------------------------------- RULES OK START ------------------------------------

    //isRecognizedCollateral works
    rule isRecognizedCollateralWorks() {
        //Function Parameters
        address collateral;

        //target result
        Type.LTVConfig collateralLTVConfig = getLTVConfigHarness(collateral);
        bool targetResult = collateralLTVConfig.targetTimestamp != 0;

        //Function call
        bool resultCall = isRecognizedCollateralHarness(collateral);

        //Assert
        assert(resultCall == targetResult, "resultCall is not targetResult");
    }

    //getLTVConfig works
    rule getLTVConfigWorks(env e){
        //Function Parameters
        address collateral;
        bool liquidation;

        //target result
        Type.LTVConfig collateralLTVConfig = getLTVConfigHarness(collateral);
        Type.ConfigAmount targetResult = getCurrentLiquidationLTV(e, collateralLTVConfig);

        //Function call
        Type.ConfigAmount resultCall = getLTVHarness(e, collateral, liquidation);

        //Assert
        //assert1: if !liquidation => resultCall == collateralLTVConfig.borrowLTV
        assert(!liquidation => resultCall == collateralLTVConfig.borrowLTV, "resultCall is not collateralLTVConfig.borrowLTV");

        //assert2: if e.block.timestamp >= collateralLTVConfig.targetTimestamp || collateralLTVConfig.liquidationLTV >= collateralLTVConfig.initialLiquidationLTV => resultCall == collateralLTVConfig.liquidationLTV
        assert(liquidation && (to_mathint(e.block.timestamp) >= to_mathint(collateralLTVConfig.targetTimestamp) || collateralLTVConfig.liquidationLTV >= collateralLTVConfig.initialLiquidationLTV) => resultCall == collateralLTVConfig.liquidationLTV, "resultCall is not collateralLTVConfig.liquidationLTV");

        //assert3: if liquidation && e.block.timestamp < collateralLTVConfig.targetTimestamp && collateralLTVConfig.liquidationLTV < collateralLTVConfig.initialLiquidationLTV => resultCall == targetResult
        assert(liquidation && to_mathint(e.block.timestamp) < to_mathint(collateralLTVConfig.targetTimestamp) && collateralLTVConfig.liquidationLTV < collateralLTVConfig.initialLiquidationLTV => resultCall == targetResult, "resultCall is not targetResult");
    } 

//------------------------------- RULES OK END ------------------------------------

