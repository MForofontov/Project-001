import React, { useState } from 'react';
import uploadFile from '../../../services/uploadFile';
import { AxiosResponse } from 'axios';
import { Button, Typography, Box } from '@mui/material';
import { styled } from '@mui/system';

const Input = styled('input')({
  display: 'none',
});

const FileUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (selectedFile) {

      const title = ``;

      // Handle file upload logic here
      uploadFile(selectedFile, title)
        .then((response: AxiosResponse<any>) => {
          console.log('File uploaded successfully:', response);
        })
        .catch((error: any) => {
          console.error('Failed to upload file:', error);
        });
    }
  };

  return (
    <div className='file-upload-container'>
      <form onSubmit={handleSubmit}>
        <Box sx={{ marginBottom: 2 }}>
          <Typography variant="h6" gutterBottom>
            Upload Music File
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <label htmlFor="file-upload">
              <Input
                accept="audio/*"
                id="file-upload"
                type="file"
                onChange={handleFileChange}
              />
              <Button variant="contained" component="span" sx={{ marginBottom: 2 }}>
                Choose File
              </Button>
            </label>
            <Button type="submit" variant="contained" color="primary">
              Upload
            </Button>
          </Box>
        </Box>
        {selectedFile && (
          <Box sx={{ marginBottom: 2 }}>
            <Typography variant="body1">Selected file: {selectedFile.name}</Typography>
            <Typography variant="body2">File size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</Typography>
          </Box>
        )}
      </form>
    </div>
  );
};

export default FileUpload;