import React, { useState } from "react";
import axios from "axios";
import styled from "styled-components";

const PageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
`;

const AppContainer = styled.div`
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 350px;
  width: 100%;
`;

const Title = styled.div`
  margin-bottom: 20px;
  font-size: 32px;
  font-weight: bold;
`;

const Subtitle = styled.div`
  margin-top: 20px;
  font-size: 24px;
  font-weight: bold;
`;

const FileInput = styled.input`
  margin-bottom: 20px;
`;

const UploadButton = styled.button`
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

const NutritionList = styled.ul`
  list-style-type: none;
  padding: 0;
`;

const NutritionItem = styled.li`
  background: #e9ecef;
  margin: 5px 0;
  padding: 10px;
  border-radius: 4px;
`;

const AlertMessage = styled.div`
  margin-top: 20px;
  padding: 10px;
  background-color: #ffcccb;
  color: #a94442;
  border: 1px solid #a94442;
  border-radius: 4px;
`;

const UploadedImage = styled.img`
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 20px;
`;

function App() {
  const [file, setFile] = useState(null);
  const [nutrition, setNutrition] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    setImageUrl(URL.createObjectURL(selectedFile));
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/predict/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setNutrition(response.data.predicted_nutrition);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <PageContainer>
      <AppContainer>
        <Title>Nutrition Prediction</Title>
        <FileInput type="file" onChange={handleFileChange} />
        <UploadButton onClick={handleUpload}>Upload</UploadButton>
        {imageUrl && (
          <div>
            <Subtitle>Uploaded Image</Subtitle>
            <UploadedImage src={imageUrl} alt="Uploaded" />
          </div>
        )}
        {nutrition && (
          <div>
            <Subtitle>Predicted Nutrition</Subtitle>
            <NutritionList>
              <NutritionItem>Carbohydrates: {nutrition[1]}</NutritionItem>
              <NutritionItem>Protein: {nutrition[2]}</NutritionItem>
              <NutritionItem>Fat: {nutrition[3]}</NutritionItem>
              <NutritionItem>Sugar: {nutrition[0]}</NutritionItem>
            </NutritionList>
            {nutrition[0] >= 5 && (
              <AlertMessage>당이 높은 음식입니다.(5이상) 주의가 필요합니다!</AlertMessage>
            )}
          </div>
        )}
      </AppContainer>
    </PageContainer>
  );
}

export default App;
