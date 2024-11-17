import grpc
from concurrent import futures
import file_metadata_pb2
import file_metadata_pb2_grpc

# In-memory storage for file metadata
file_metadata_store = []

class FileMetadataService(file_metadata_pb2_grpc.FileMetadataServiceServicer):
    def UploadMetadata(self, request, context):
        file_metadata_store.append(request)
        print(f"Received metadata: {request}")
        return file_metadata_pb2.Empty()

    def ListMetadata(self, request, context):
        for metadata in file_metadata_store:
            yield metadata

    def GetMetadataByName(self, request, context):
        for metadata in file_metadata_store:
            if metadata.file_name == request.file_name:
                return metadata
        context.abort(grpc.StatusCode.NOT_FOUND, "File not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_metadata_pb2_grpc.add_FileMetadataServiceServicer_to_server(FileMetadataService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()