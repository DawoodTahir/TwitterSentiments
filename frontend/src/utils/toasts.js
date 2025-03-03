import { toast } from "react-toastify";

export const showToast = {
    success: (message) => toast.success(message),
    error: (message) => toast.error(message),
    info: (message) => toast.info(message),
    loading: (message) => {
      const toastId = toast.loading(message); 
      return toastId; 
    },
    dismiss: (toastId) => toast.dismiss(toastId), 
  };
  