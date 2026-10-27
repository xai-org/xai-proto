package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"
)

func main() {
	// Get API key from environment
	apiKey := os.Getenv("XAI_API_KEY")
	if apiKey == "" {
		log.Println("⚠️  XAI_API_KEY not set. Using placeholder.")
		apiKey = "your-api-key-here"
	}

	// Connect to xAI API
	conn, err := grpc.NewClient(
		"api.x.ai:443",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	fmt.Println("✅ Successfully created gRPC client")
	fmt.Println("📦 Generated Go code location: gen/go/xai/api/v1/")
	fmt.Println("")
	fmt.Println("Example usage:")
	fmt.Println("  import xaiv1 \"github.com/xai-org/xai-proto/gen/go/xai/api/v1\"")
	fmt.Println("  client := xaiv1.NewLanguageServiceClient(conn)")
	fmt.Println("  // Make API calls with the client")
	fmt.Println("")
	fmt.Println("For full API documentation, visit: https://docs.x.ai/")

	// Create context with API key
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	_ = metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+apiKey)

	fmt.Println("")
	fmt.Println("🚀 Go SDK is ready to use!")
	fmt.Println("💡 To use the generated services, import:")
	fmt.Println("   xaiv1 \"github.com/xai-org/xai-proto/gen/go/xai/api/v1\"")
}