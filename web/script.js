document.addEventListener('DOMContentLoaded', () => {
    const viewDetailsButtons = document.querySelectorAll('.view-details');
  
    viewDetailsButtons.forEach(button => {
      button.addEventListener('click', () => {
        const jobIndex = button.dataset.jobId;
        const jobData = jobData[jobIndex - 1]; // Adjust index as needed
  
        const jobDetailsDiv = document.getElementById('job-details');
        jobDetailsDiv.style.display = 'block';
  
        document.getElementById('job-title').textContent = jobData.title;
        document.getElementById('job-company').textContent = jobData.company;
        // ... set other details similarly
        document.getElementById('job-desc').textContent = jobData.job_desc;
      });
    });
  });