# gRPC Calculator Project

This project implements a simple calculator using gRPC, structured in a client-server architecture. The calculator supports basic arithmetic operations: addition, subtraction, multiplication, and division.

## Project Structure

```
grpc-calculator
├── proto
│   └── calculator.proto        # Protocol Buffers definition for the calculator service
├── packages
│   ├── server                  # Server-side implementation
│   │   ├── src
│   │   │   ├── server.ts       # Entry point for the gRPC server
│   │   │   ├── services
│   │   │   │   └── calculatorService.ts  # Implementation of the Calculator service
│   │   │   └── utils
│   │   │       └── logger.ts   # Utility functions for logging
│   │   ├── tests
│   │   │   └── calculator.service.spec.ts  # Unit tests for the Calculator service
│   │   ├── package.json         # Server package configuration
│   │   └── tsconfig.json        # TypeScript configuration for the server
│   ├── client                   # Client-side implementation
│   │   ├── src
│   │   │   ├── client.ts        # Entry point for the gRPC client
│   │   │   └── commands
│   │   │       └── calcCommand.ts  # Command handling for the client
│   │   ├── tests
│   │   │   └── client.spec.ts   # Unit tests for the client
│   │   ├── package.json         # Client package configuration
│   │   └── tsconfig.json        # TypeScript configuration for the client
│   └── shared                   # Shared utilities and proto loading
│       ├── src
│       │   └── proto-loader.ts  # Loads the proto definitions
│       ├── tests
│       │   └── proto-loader.spec.ts  # Unit tests for proto loading
│       ├── package.json         # Shared package configuration
│       └── tsconfig.json        # TypeScript configuration for shared code
├── .gitignore                   # Git ignore file
├── package.json                 # Root package configuration
├── tsconfig.json                # Root TypeScript configuration
└── README.md                    # Project documentation
```

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- gRPC and Protocol Buffers knowledge is helpful but not required.

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd grpc-calculator
   ```

2. Install dependencies for both server and client:
   ```
   cd packages/server
   npm install
   cd ../client
   npm install
   ```

### Generating Protocol Buffers Stubs

Run the following script to generate the necessary gRPC stubs from the `.proto` file:
```
cd scripts
bash gen_stubs.sh
```

### Running the Server

To start the gRPC server, run:
```
cd packages/server
npm start
```

### Running the Client

In a new terminal, run the client:
```
cd packages/client
npm start
```

### Running Tests

To execute the unit tests, navigate to each package and run:
```
cd packages/server
npm test
cd ../client
npm test
```

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.