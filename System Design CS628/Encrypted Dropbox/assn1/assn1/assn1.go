package assn1

// You MUST NOT change what you import.  If you add ANY additional
// imports it will break the autograder, and we will be Very Upset.
//
import (
	// You neet to add with
	// go get github.com/sarkarbidya/CS628-assn1/userlib
	"github.com/sarkarbidya/CS628-assn1/userlib"
	// Life is much easier with json:  You are
	// going to want to use this so you can easily
	// turn complex structures into strings etc...
	"encoding/json"
	// Likewise useful for debugging etc
	"encoding/hex"
	// UUIDs are generated right based on the crypto RNG
	// so lets make life easier and use those too...
	//
	// You need to add with "go get github.com/google/uuid"
	"github.com/google/uuid"
	// Useful for debug messages, or string manipulation for datastore keys
	"strings"

	// Want to import errors
	"errors"
)

// This serves two purposes: It shows you some useful primitives and
// it suppresses warnings for items not being imported
func someUsefulThings() {
	// Creates a random UUID
	f := uuid.New()
	userlib.DebugMsg("UUID as string:%v", f.String())

	// Example of writing over a byte of f
	f[0] = 10
	userlib.DebugMsg("UUID as string:%v", f.String())

	// takes a sequence of bytes and renders as hex
	h := hex.EncodeToString([]byte("fubar"))
	userlib.DebugMsg("The hex: %v", h)

	// Marshals data into a JSON representation
	// test
	// Will actually work with go structures as well
	d, _ := json.Marshal(f)
	userlib.DebugMsg("The json data: %v", string(d))
	var g uuid.UUID
	json.Unmarshal(d, &g)
	userlib.DebugMsg("Unmashaled data %v", g.String())

	// This creates an error type
	userlib.DebugMsg("Creation of error %v", errors.New(strings.ToTitle("This is an error")))

	// And a random RSA key.  In this case, ignoring the error
	// return value
	var key *userlib.PrivateKey
	key, _ = userlib.GenerateRSAKey()
	userlib.DebugMsg("Key is %v", key)
}

var configBlockSize = 4096 //Do not modify this variable

//setBlockSize - sets the global variable denoting blocksize to the passed parameter. This will be called only once in the beginning of the execution
func setBlockSize(blocksize int) {
	configBlockSize = blocksize
}

// Helper function: Takes the first 16 bytes and
// converts it into the UUID type
func bytesToUUID(data []byte) (ret uuid.UUID) {
	for x := range ret {
		ret[x] = data[x]
	}
	return
}

//User : User structure used to store the user information
type User struct {
	Username      string
	Password      string
	RSAPrivateKey userlib.PrivateKey
	HashUsername  []byte
	HashPassword  []byte
	FileHash      map[string][]byte          
	FileKey       map[string][]byte
	//hits := make(map[string]map[string]int)
	// You can add other fields here if you want...
	// Note for JSON to marshal/unmarshal, the fields need to
	// be public (start with a capital letter)
}

func (userdata *User) StoreFile(filename string, data []byte) (err error) {
	
	hash,ok := userdata.FileHash[filename]
  
	if(!ok)	{
	if (len(data) % configBlockSize) != 0 {
		err = errors.New("File size should be multiple of block length")
	} else {
		Key := userlib.RandomBytes(userlib.BlockSize)
		CFBKey := userlib.RandomBytes(userlib.BlockSize)
		
		numberOfBlocks := (len(data) / configBlockSize)

		var file sharingRecord
		file.CFBKey = CFBKey
		file.FileLength = numberOfBlocks
		file.BlockHash = make(map[int][]byte)
		file.BlockMAC = make(map[int][]byte)
		file.BlockIV = make(map[int][]byte)
	
		for i := 0; i < numberOfBlocks; i++ {
			iv := userlib.RandomBytes(userlib.BlockSize)
			file.BlockIV[i]=iv
		
			ciphertext := make([]byte, configBlockSize)

			cipher := userlib.CFBEncrypter(CFBKey, iv)
			cipher.XORKeyStream(ciphertext, data[i*configBlockSize:(i+1)*configBlockSize])

			mac := userlib.NewHMAC(CFBKey)
			mac.Write(ciphertext)
			DataBlockMac := mac.Sum(nil)
			file.BlockHash[i] = userlib.RandomBytes(16)
			file.BlockMAC[i] = DataBlockMac
			userlib.DatastoreSet(string(file.BlockHash[i]), ciphertext)

		}
		f, _ := json.Marshal(&file)
		ciphertext := make([]byte, userlib.BlockSize+len(f))
		iv := ciphertext[:userlib.BlockSize]
		copy(iv, userlib.RandomBytes(userlib.BlockSize))
		cipher := userlib.CFBEncrypter(Key, iv)
		cipher.XORKeyStream(ciphertext[userlib.BlockSize:], []byte(f))

		mac := userlib.NewHMAC(Key)
		mac.Write(ciphertext)
		FileMac := mac.Sum(nil)
		
		userlib.DatastoreSet(string(FileMac), ciphertext)

		userdata.FileHash = make(map[string][]byte)
		userdata.FileHash[filename] = FileMac
		userdata.FileKey = make(map[string][]byte)
		userdata.FileKey[filename] = Key

	}
} else{
	
	if (len(data) % configBlockSize) == 0 {
		encryptedSharingData, valid := userlib.DatastoreGet(string(hash))
		if !valid {
			err = errors.New("Improper fetch")
		} else {	
			    Key := userdata.FileKey[filename]
				
				iv := encryptedSharingData[:userlib.BlockSize]
				ciphertext := encryptedSharingData
				cipher := userlib.CFBDecrypter(Key, iv)
				cipher.XORKeyStream(ciphertext[userlib.BlockSize:], ciphertext[userlib.BlockSize:])

				numberOfBlocks := len(data) / configBlockSize

				var file sharingRecord
				json.Unmarshal(ciphertext[userlib.BlockSize:], &file)

				CFBKey:=file.CFBKey
				file.FileLength = numberOfBlocks
				file.BlockHash=nil	
				file.BlockHash = make(map[int][]byte)
				file.BlockMAC=nil
				file.BlockMAC = make(map[int][]byte)
				file.BlockIV=nil
				file.BlockIV = make(map[int][]byte)
				for i := 0; i < numberOfBlocks; i++ {
					iv := userlib.RandomBytes(userlib.BlockSize)
					file.BlockIV[i]=iv
				
				ciphertext := make([]byte, configBlockSize)

				cipher := userlib.CFBEncrypter(CFBKey, iv)
				cipher.XORKeyStream(ciphertext, data[i*configBlockSize:(i+1)*configBlockSize])

				mac := userlib.NewHMAC(CFBKey)
				mac.Write(ciphertext)
				DataBlockMac := mac.Sum(nil)

				file.BlockMAC[i] = DataBlockMac
				file.BlockHash[i] = userlib.RandomBytes(16)
				userlib.DatastoreSet(string(file.BlockHash[i]), ciphertext)
				}
			
				f, _ := json.Marshal(&file)
				ciphertext = make([]byte, userlib.BlockSize+len(f))
				iv = ciphertext[:userlib.BlockSize]
				copy(iv, userlib.RandomBytes(userlib.BlockSize))
				cipher = userlib.CFBEncrypter(Key, iv)
				cipher.XORKeyStream(ciphertext[userlib.BlockSize:], []byte(f))

				userlib.DatastoreSet(string(hash), ciphertext)
			
	}   
	}else{
		err=errors.New("Data should be multiple of block size")
	}


}
	return err

}

func (userdata *User) AppendFile(filename string, data []byte) (err error) {

	if (len(data) % configBlockSize) == 0 {
		
		hash,ok := userdata.FileHash[filename]
		if(!ok){
			err=errors.New("File does not exist")
		} else {		
		encryptedSharingData, valid := userlib.DatastoreGet(string(hash))
		if !valid {
			err = errors.New("Improper fetch")
		} else {
				Key := userdata.FileKey[filename]
				iv := encryptedSharingData[:userlib.BlockSize]
				ciphertext := encryptedSharingData
				cipher := userlib.CFBDecrypter(Key, iv)
				cipher.XORKeyStream(ciphertext[userlib.BlockSize:], ciphertext[userlib.BlockSize:])

				numberOfBlocks := len(data) / configBlockSize

				var fileRecord sharingRecord
				json.Unmarshal(ciphertext[userlib.BlockSize:], &fileRecord)

				for i := 0; i < numberOfBlocks; i++ {
					iv := userlib.RandomBytes(userlib.BlockSize)
					fileRecord.BlockIV[fileRecord.FileLength+i]=iv
					ciphertext := make([]byte, configBlockSize)

					cipher := userlib.CFBEncrypter(fileRecord.CFBKey, iv)
					cipher.XORKeyStream(ciphertext, data[i*configBlockSize:(i+1)*configBlockSize])

					mac := userlib.NewHMAC(fileRecord.CFBKey)
					mac.Write(ciphertext)
					DataBlockMac := mac.Sum(nil)

					fileRecord.BlockMAC[fileRecord.FileLength+i] = DataBlockMac
					fileRecord.BlockHash[fileRecord.FileLength+i] = userlib.RandomBytes(16)
					userlib.DatastoreSet(string(fileRecord.BlockHash[fileRecord.FileLength+i]), ciphertext)
				}
				
				fileRecord.FileLength = fileRecord.FileLength + numberOfBlocks
				f, _ := json.Marshal(&fileRecord)
				ciphertext = make([]byte, userlib.BlockSize+len(f))
				iv = ciphertext[:userlib.BlockSize]
				copy(iv, userlib.RandomBytes(userlib.BlockSize))
				cipher = userlib.CFBEncrypter(Key, iv)
				cipher.XORKeyStream(ciphertext[userlib.BlockSize:], []byte(f))

				userlib.DatastoreSet(string(hash), ciphertext)
			
		}
	} 	
	}else{
		err=errors.New("Data should be multiple of block size")
	}

	return err
}
func (userdata *User) LoadFile(filename string, offset int) (data []byte, err error) {
	hash, ok := userdata.FileHash[filename]
	if !ok {
		data = nil
	} else {
		encryptedSharingData, valid := userlib.DatastoreGet(string(hash))
		if !valid {
			err = errors.New("File record corrupted")
		} else {
			Key := userdata.FileKey[filename]
		    iv := encryptedSharingData[:userlib.BlockSize]
				ciphertext := encryptedSharingData
				cipher := userlib.CFBDecrypter(Key, iv)
				cipher.XORKeyStream(ciphertext[userlib.BlockSize:], ciphertext[userlib.BlockSize:])
			
				var fileRecord sharingRecord
				json.Unmarshal(ciphertext[userlib.BlockSize:], &fileRecord)
				_,ok:=fileRecord.BlockHash[offset]
				if ok{
				encryptedFileData, valid := userlib.DatastoreGet(string(fileRecord.BlockHash[offset]))
			
				if !valid {
					err = errors.New("File corrupted")
				} else {
					mac := userlib.NewHMAC(fileRecord.CFBKey)
					mac.Write(encryptedFileData)
					BlockMac := mac.Sum(nil)
					if !userlib.Equal(BlockMac, fileRecord.BlockMAC[offset]) {
						err = errors.New("File Block corrupted")
					} else {
						ciphertext := encryptedFileData
						cipher := userlib.CFBDecrypter(fileRecord.CFBKey, fileRecord.BlockIV[offset])
						cipher.XORKeyStream(ciphertext, ciphertext)
						data = ciphertext
					}
				}
			}else{
				err= errors.New("Invalid offset")
			}
		}

		
	}
	return data, err

}

func (userdata *User) ShareFile(filename string, recipient string) (msgid string, err error) {
	Key,ok := userdata.FileKey[filename]
	if ok{
	Hash := userdata.FileHash[filename]
	msg := append(Key[:], Hash[:]...)
	var bytes []byte
	sign, err := userlib.RSASign(&userdata.RSAPrivateKey, msg)
	if err == nil {
		key, ok := userlib.KeystoreGet(recipient)
		if(ok){
		bytes, err = userlib.RSAEncrypt(&key, msg, []byte("Tag"))
		msgid = string(append(sign[:], bytes[:]...))
		}  else {
			err=errors.New("Reciever not found")
		}
	}
    }else{
	err=errors.New("File not found")
    }	
	return msgid, err
}

func (userdata *User) ReceiveFile(filename string, sender string, msgid string) error {
    decrypt, err := userlib.RSADecrypt(&userdata.RSAPrivateKey, []byte(msgid)[256:], []byte("Tag"))
	key, ok := userlib.KeystoreGet(sender)
	if ok {
		e := userlib.RSAVerify(&(key), decrypt, []byte(msgid[0:256]))
		if e==nil{
		hash := []byte(decrypt[16:])
		CFBkey := []byte(decrypt[0:16])
		_, valid :=userlib.DatastoreGet(string(hash))
			if(valid){
		if len(userdata.FileHash)==0 {
		userdata.FileHash = make(map[string][]byte)
		userdata.FileKey = make(map[string][]byte)
		}
		userdata.FileHash[filename] = hash
		userdata.FileKey[filename] = CFBkey
		}else {
			err=errors.New("File Record not found")
		}	
	}else{
		err=e
	}
	}else{
		err= errors.New("Sender not found")
	}
	return err

}

func (userdata *User) RevokeFile(filename string) (err error) {
	hash, ok := userdata.FileHash[filename]
	if ok {
		encryptedSharingData, valid := userlib.DatastoreGet(string(hash))
		if valid {
			Key := userdata.FileKey[filename]
			mac := userlib.NewHMAC(Key)
			mac.Write(encryptedSharingData)
			FileMac := mac.Sum(nil)
			    iv := encryptedSharingData[:userlib.BlockSize]
				Record := encryptedSharingData
				cipher := userlib.CFBDecrypter(Key, iv)
				cipher.XORKeyStream(Record[userlib.BlockSize:], Record[userlib.BlockSize:])
				var file sharingRecord
				json.Unmarshal(Record[userlib.BlockSize:], &file)
				newKey := userlib.RandomBytes(userlib.BlockSize)
				f, _ := json.Marshal(&file)
				
				
				ciphertext := make([]byte, userlib.BlockSize+len(f))
				iv = ciphertext[:userlib.BlockSize]
				copy(iv, userlib.RandomBytes(userlib.BlockSize))
				cipher = userlib.CFBEncrypter(newKey, iv)
				cipher.XORKeyStream(ciphertext[userlib.BlockSize:], f)
				
				
				userlib.DatastoreDelete(string(hash))
				
				mac = userlib.NewHMAC(newKey)
				mac.Write(ciphertext)
				FileMac = mac.Sum(nil)
				
				userlib.DatastoreSet(string(FileMac), ciphertext)
				
				userdata.FileHash[filename] = FileMac
				userdata.FileKey[filename] = newKey
			
		} else{
			err=errors.New("File corrupted")
		}
	} else{
		err=errors.New("File does not exist")
	}
	return err
}

type sharingRecord struct {
	FileLength int
	BlockHash  map[int][]byte
	BlockMAC map[int][]byte
	BlockIV  map[int][]byte
	CFBKey     []byte
}

//var iv []byte
func InitUser(username string, password string) (userdataptr *User, err error) {

	usernameByte := []byte(username)
	passwordByte := []byte(password)
	s := "1"
	passLength := len(passwordByte)
	if passLength > 0 {
		if len(passwordByte) < userlib.AESKeySize {
			for i := 0; i < userlib.AESKeySize-passLength; i++ {
				passwordByte = append(passwordByte[:], s...)
			}
		} else if len(passwordByte) > userlib.AESKeySize {
			passwordByte = passwordByte[0:15]
		}
		mac := userlib.NewHMAC(passwordByte)
		mac.Write(usernameByte)
		usernameMac := mac.Sum(nil)
		
		mac = userlib.NewHMAC(passwordByte)
		mac.Write(passwordByte)
		passwordMac := mac.Sum(nil)
		_, valid := userlib.DatastoreGet(string(usernameMac))
		if valid {
			err = errors.New("Invalid User")
		} else {
			
		rsakey, err := userlib.GenerateRSAKey()
		if err != nil {
			err = errors.New("Got RSA error")
		}
		
		pubkey := rsakey.PublicKey
		userlib.KeystoreSet(username, pubkey)

		user := User{username, string(passwordByte), *rsakey, usernameMac, passwordMac, nil, nil}

		u, _ := json.Marshal(&user)
		ciphertext := make([]byte, userlib.BlockSize+len(u))

		iv := ciphertext[:userlib.BlockSize]
		copy(iv, userlib.RandomBytes(userlib.BlockSize))

		cipher := userlib.CFBEncrypter(passwordByte, iv)
		cipher.XORKeyStream(ciphertext[userlib.BlockSize:], []byte(u))
		userlib.DatastoreSet(string(usernameMac), ciphertext)
		
		userdataptr = &user
	} 
	}  else {
		err = errors.New("Please provide valid username and password")
	}
	return userdataptr, err
}

// GetUser : This fetches the user information from the Datastore.  It should
// fail with an error if the user/password is invalid, or if the user
// data was corrupted, or if the user can't be found.
//GetUser : function used to get the user details
func GetUser(username string, password string) (userdataptr *User, err error) {
	usernameByte := []byte(username)
	passwordByte := []byte(password)
	s := "1"
	passLength := len(passwordByte)
	if passLength > 0 {
		if len(passwordByte) < userlib.AESKeySize {
			for i := 0; i < userlib.AESKeySize-passLength; i++ {
				passwordByte = append(passwordByte[:], s...)
			}
		} else if len(passwordByte) > userlib.AESKeySize {
			passwordByte = passwordByte[0:15]
		}
		mac := userlib.NewHMAC(passwordByte)
		mac.Write(usernameByte)
		usernameMac := mac.Sum(nil)

		mac = userlib.NewHMAC(passwordByte)
		mac.Write(passwordByte)
		passwordMac := mac.Sum(nil)
		

		encryptdData, valid := userlib.DatastoreGet(string(usernameMac))
		
		if !valid {
			err = errors.New("Invalid User")
		} else {
			iv := encryptdData[:userlib.BlockSize]
			ciphertext := encryptdData

			cipher := userlib.CFBDecrypter(passwordByte, iv)
			cipher.XORKeyStream(ciphertext[userlib.BlockSize:], ciphertext[userlib.BlockSize:])

			var g User

			json.Unmarshal(ciphertext[userlib.BlockSize:], &g)
			if !userlib.Equal(usernameMac, g.HashUsername) {
				err = errors.New("Data corrupted")
			}
			if !userlib.Equal(passwordMac, g.HashPassword) {
				err = errors.New("Data corrupted")
			}
			userdataptr = &g
		}
	} else {
		err = errors.New("Invalid user")
	}

	return userdataptr, err
}

