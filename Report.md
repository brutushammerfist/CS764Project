# CS764 Project - Matthew Perry - Spring 2021

When beginning my work on this project, I had not realized that the blockchain in question was to be built on top of Ethereum using Smart Contracts. So, I had originally started this project as a Python implementation of a blockchain. Thankfully, I had not gotten too far when rereading the assignment instructions and was able to swap over to Solidity Smart Contracts.

Due to a severe lack of time to put into this project, I have decided that it would be best to forego the fancy frontend webpages and simply create the functioning Blockchain within the remix online editor at [remix.ethereum.org](remix.ethereum.org).

I will attempt to go over any major assumptions for each piece of functionality within this report, but if I miss something it will be documented in comments within the code. One overall assumption that I have made is that financial transactions (such as paying the fees for titling a vehicle, etc.) are handled on a separate system and this blockchain will only be called once those payments have been processed.

On a final note before we move on to implementation details and lessons learned, much of this project ended up being fairly confusing in regard to exactly what was expected for each of the services that we were to implement. Some items that were expected to be implemented were copies of each other essentially, one having some more information on the webpage than the other, but ultimately point to the other. In future iterations of this project, I would like to see some more explanation about what exactly is expected for these.

## **Implementation Details**

To keep things simple, I decided it best to write everything in a single Solidity Smart Contract, titled DMV. The following image shows the necessary data structures and the constructor for the contract.

```solidity
    /**
     * Data Structures
     */
    
    uint public vehicleVIN = 0;
    
    struct Driver {
        address driver;
        bool hasRealID;
        uint licenseGoodUntil;
        string addr;
        uint practiceExamScore;
    }
    
    struct Vehicle {
        uint vin;
        address owner;
        uint registrationGoodUntil;
        bool titled;
        bool sold;
    }
    
    mapping(address => Driver) public drivers;
    
    mapping(uint => Vehicle) public vehicles;
```

The vehicleVIN variable acts as a counter, incrementing by one each time a new vehicle is titled. This is then used as a unique identifier for the vehicle when looking it up in the system. It is of type uint for simplicity here, but real life VINs can have both letters and numbers in them, meaning that an actual representation would likely need to be a string of some kind.

The two structs, Driver and Vehicle, hold information about their respective entities. A Driver has information about the driver themselves, such as when their license expires, or their street address. A Vehicle holds information about a vehicle, such as if it has been reported as sold, or who the owner is.

Then, two maps are created to hold instances of the Driver and Vehicle structs, as well as give an easy way access this information, via the owner's address and the vehicle's VIN. Maps in Solidity work slightly differently than maps in other languages. All possibilities for key values are initialized to zero in all fields of the struct, meaning that we don't have to initialize the map with data and can simply update the data.

```solidity
    function addVehicle (address _owner) public {
        vehicleVIN++;
        vehicles[vehicleVIN] = Vehicle(vehicleVIN, _owner, 0, false, false);
    }
```

A helper function, `addVehicle`, simply takes the required information to update the instance of the Vehicle struct that matches its VIN. The vin and owner fields of the struct are updated, while the others remain their default values.

### **Online Services**

```solidity
    /**
    *  Online Services
    */
    
    function renewVehicleReg (uint _vin) public returns (string memory) {
        /**
         * Vehicle Registation renewals vary in length. From the website, you can renew for either 1 or 2 years at a time.
         * I've opted to assume that user's will always go with the longer renewal option, for simplicity.
         * 
         * Before renewing, the Requestor is verified to be the owner of the vehicle.
         */
         
        require(vehicles[_vin].owner == msg.sender, "Requestor is not owner of vehicle.");
        vehicles[_vin].registrationGoodUntil = block.timestamp + (2 * 365 days);
        return "Vehicle registration successfully renewed.";
    }
    
    function changeAddress (string memory _address, bool _canBeVerified) public returns (string memory) {
        /**
         * There are cases, especially when moving between states, where information needs to be verified/proven,
         * such as legal presence when moving TO Virginia. Because of this, the information will need to be verified
         * with an outside system before records can be changed.
         * 
         * For now, seeing as we cannot actually verify the data, the _canBeVerified parameter 
         * will act as the verification result.
         */
        
        require(_canBeVerified == true, "The supplied information cannot be verified. Please check for any errors or contact a representative if everything is correct.");
        drivers[msg.sender].addr = _address;
        return "Your address has been successfully updated.";
    }
    
    function renewDriversLicense () public returns (string memory) {
        /**
         * Driver's License renewals vary in length. From the website, you can renew for either 5 or 8 years at a time.
         * Just as with the Vehicle Registration, I've opted to assume that user's will always go with the longer renewal option.
         */
        
        drivers[msg.sender].licenseGoodUntil = block.timestamp + (8 * 365 days);
        return "Driver's License successfully renewed.";
    }
    
    function reportSoldOrTradedVehicle (uint _vin) public returns (string memory) {
        /**
         * The owner of the vehicle is reporting their vehicle as sold or traded.
         * Set owner to "null" since we do not yet know who the new owner is (need to wait for them to title the vehicle).
         * 
         * First checks to ensure that the Requestor is the owner of the vehicle that they are attempting to report on.
         */
        
        require(vehicles[_vin].owner == msg.sender, "Requestor is not owner of vehicle.");
        delete vehicles[_vin].owner;
        vehicles[_vin].sold = true;
        return "Vehicle has been reported as sold.";
    }
```

#### **Renew Vehicle Registration**

According to the DMV website, vehicle registrations can be renewed in intervals of one or two years only. I've decided to assume, then, that customer's will always renew their registration for the full two years. Before the system renews the registration, it makes a check to ensure that the individual requesting the renewal is the owner of said vehicle. If the requestor is not the owner of the vehicle, the registration is not renewed. If they are, the expiration date of the registration is updated to two years from the current time.

#### **Change Address**

Changing your address at the DMV can sometimes require proof of the new address. With that being the case, I've decided that this information will likely need to be verified in a separate system. To simulate this verification, a boolean is passed into the function, rather than the actual information, that acts as the result of the verification process. You will see that I have done this in several other functions later on as well. If the verification was successful, the address of the driver is updated, and nothing is changed if the verificated was not successful.

#### **Renew Driver's License**

Driver's license renewal was very simple, as the expiration time of the license simply needed updating. Since the requestor's address is used to access their records, there's no need to check if they're allowed to change the record, seeing as it is their own. Just as with the vehicle registration, I've opted to assume that customers are renewing for the maximum amount of time, being eight years, rather than five.

#### **Report Vehicle Sold or Traded**

This and the Sell or Donate Vehicle are the exact same in my implementation. This is because the Sell or Donate Vehicle page on the DMV site actively points you to the Report your Vehicle Sold page, just with some more information on the page. Here, once the requestor is verified to be the owner of the vehicle, the owner is set to "null" (in this case, its the zero address), and the sold flag is set to true on the vehicle.

### **Driver's License/Identification Services**

```solidity
    /**
     * Drivers License/Identification Services
     */
     
    function practiceExam (uint _score) public returns (string memory) {
        /**
         * As I'm fairly certain that the DMV doesn't retain any of the scores for the these online practice exams,
         * I wasn't sure how to actually go about implementing this. I've opted to say that a driver's record holds
         * the highest value gotten by the driver on these practice exams.
         */
        
        if (_score > drivers[msg.sender].practiceExamScore) {
            drivers[msg.sender].practiceExamScore = _score;
        }
        return "Your exam score has been recorded.";
    }
    
    function realID (bool _canBeVerified) public returns (string memory) {
        require(drivers[msg.sender].driver == msg.sender, "Requestor does not match the driver on record.");
        /**
         * Information for this should be passed in to be verified elsewhere. This information contains the following:
         * 
         *  - Full Legal Name
         *  - SNN
         *  - Birthdate
         *  - Address, City, and State
         *  - Email Address
         *  - And much more...
         * 
         * For now, seeing as we cannot actually verify the data, the _canBeVerified parameter 
         * will act as the verification result.
         */
        
        require(_canBeVerified == true, "The supplied information cannot be verified. Please check for any errors or contact a representative if everything is correct.");
        drivers[msg.sender].hasRealID = true;
        return "Your information has been verified and your RealID will be mailed to you at the address on file. Please allow up to 15 days before contacting the DMV about missing documents.";
    }
    
    function obtainRecord(bool _canBeVerified) public pure returns (string memory) {
        /**
         * Records assumed to be Social Security Card or replacement ID card,
         * as those are the only ones that a copy/reissue can be requested for.
         * 
         * Information should be verified from another source, such as SSA or elsewhere.
         * 
         * Required Information:
         *  - SSN
         *  - Birthdate
         *  - Maybe more.
         * 
         * For now, seeing as we cannot actually verify the data, the _canBeVerified parameter 
         * will act as the verification result.
         */
         
        require(_canBeVerified == true, "The supplied information cannot be verified. Please check for any errors or contact a representative if everything is correct.");
        return "Your new document will be mailed to you at the address on file. Please allow up to 15 days before contacting the DMV about missing documents.";
    }
```

#### **Practice Exams**

As far as the practice exams go, it wasn't clear what exactly was being asked of me. I had two thoughts when attempting to create this service: retain the scores of the practice exams that each driver takes or return the set of questions that should be asked to the driver. Opting to not have another fake outside system to deal with, I added a variable in the Driver struct that stores the highest ever exam score that the driver has earned.

#### **RealID**

For this service, I thought of it as putting in an application to receive a RealID. In order to obtain a RealID, many different documents are required when applying. These documents in our blockchain system, would be verified in an outside source. With that in mind, I took the same approach as I had for changing a driver's address and there is a parameter for the function that tells us if the documents were able to be verified or not. If it can be verified, the drivers records are updated to show that they now hold a RealID.

#### **Obtain Vital Record**

Checking the DMV website, the online records that you can request to obtain from them are a new Social Security Card or a replacement ID card. Looking into Medical Information, there was nothing to request or applications to submit. It was simply a trove of information about the medical requirements and standards for driving.

### Vehicle Services

```solidity
    /**
     * Vehicle Services
     */
     
    function sellOrDonateVehicle (uint _vin) public returns (string memory) {
        /**
         * I see no difference between this and reporting a vehicle as sold or traded.
         * 
         * The owner of the vehicle is reporting their vehicle as sold or donated.
         * Set owner to "null" since we do not yet know who the new owner is (need to wait for them to title the vehicle).
         * 
         * First checks to ensure that the Requestor is the owner of the vehicle that they are attempting to report on.
         */
        
        require(vehicles[_vin].owner == msg.sender, "Requestor is not owner of vehicle.");
        delete vehicles[_vin].owner;
        vehicles[_vin].sold = true;
        return "Vehicle has been reported as sold.";
    }
    
    function titleVehicle (uint _vin) public returns (string memory) {
        /**
         * This assumes that the user attempting to title a vehicle that already exists
         * has the old title that has been signed over to them or bill of sale, etc.
         */
         
        if (_vin == 0) {
            // New Vehicle
            addVehicle(msg.sender);
        } else {
            // Vehicle exists, transfer title to msg.sender
            require(vehicles[_vin].sold == true, "Vehicle has not been marked as sold, cannot transfer title.");
            vehicles[_vin].owner = msg.sender;
            vehicles[_vin].sold = false;
        }
        return "Vehicle has successfully been titled.";
    }
```

#### **Sell or Donate Vehicle**

As stated previously in the Report Vehicle Sold or Traded section, I saw no difference between this service and that one. Especially seeing as the DMV page for this services links to that service. Therefore, the code here is exactly the same as the previous functions and operates the same way.

#### **Title Vehicle**

For titling a vehicle, there seemed to be two outcomes. Either the vehicle was brand new and would need to be added to the map of current vehicles, or the vehicle was sold and is now being retitled by the new owner. This function takes in a VIN, and if this VIN is zero, that represents this being a brand new vehicle and said vehicle is added to the map with the requestor as the owner. If the VIN is not zero, then the vehicle should have been reported as sold by the previous owner, so that the new owner can title the vehicle.

## **Lessons Learned**

Seeing as the only experience that I have with Solidity are the Module 7 Homework and this project, I am certain that there are plenty of best practices or expertise that I know nothing about. It still surprises me to this day how much I still learn about languages such as C++. I don't, however, see myself continuing further in this scope of programming, so I will likely not get to understand how to better perform certain tasks.

Other than the exposure to the Ethereum network and how to create systems on top of the Ethereum blockchain, I'm honestly lost as to what lessons were to be provided from this project. This is not an inherently bad thing, as exposure and experience working with a system can be a great asset moving into the future. This project gave me a better understand about how Smart Contracts can be utilized to build systems ontop of the blockchain, and while I may not find use for this knowledge later on, I do believe that it was a fun and interesting experience, which is enough for me.