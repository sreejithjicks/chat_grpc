import grpc
import file_metadata_pb2
import file_metadata_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = file_metadata_pb2_grpc.FileMetadataServiceStub(channel)

    # Upload metadata
    metadata = file_metadata_pb2.FileMetadata(
        file_name="example.png",
        file_size=1024,
        file_type="image/png"
    )
    stub.UploadMetadata(metadata)
    print("Uploaded metadata for 'example.png'")

    print("\nListing all metadata:")
    for file_metadata in stub.ListMetadata(file_metadata_pb2.Empty()):
        print(f"{file_metadata.file_name} - {file_metadata.file_size} bytes - {file_metadata.file_type}")

    try:
        response = stub.GetMetadataByName(
            file_metadata_pb2.GetMetadataRequest(file_name="example.png")
        )
        print(f"\nMetadata for 'example.png': {response}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")

if __name__ == "__main__":
    run()